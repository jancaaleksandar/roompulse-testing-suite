import re
from typing import Any, cast

from hotel_info_lib import ProcessRequestParsingTask, log
from selectolax.parser import HTMLParser, Node

from ..types.offer import BookingChoice, Offer


class BookingPriceParserMobile:
    def __init__(self, response: str, task: ProcessRequestParsingTask) -> None:
        self.response = response
        self.task = task

    def parse(self) -> dict[str, Any]:
        try:
            doc = HTMLParser(self.response)
            rooms: list[Offer] = []

            # Check if results should be for authenticated user
            sign_in_button = doc.css_first('[data-testid="header-sign-in-button"]')
            if str(self.task.task__parsing_price_variables_rates_type) == "MEMBER" and sign_in_button:
                log(
                    log_message="Results are for not authenticated user even if authenticated user results requested",
                    log_path="app/booking_price_mobile_parser.py | parse",
                    individual_id=cast(int, self.task.task_id),
                )

            # Look for mobile rooms table
            rooms_table = doc.css_first(".db-section__rooms-table")

            if rooms_table:
                room_elements = rooms_table.css(".db-card__room")
                if room_elements:
                    rooms = self._extract_rooms_from_mobile_cards(room_elements)

        except (ValueError, KeyError, AttributeError, TypeError) as e:
            log(
                log_message=f"Parsing failed: {e!s}",
                log_path="app/booking_price_mobile_parser.py | parse",
                individual_id=cast(int, self.task.task_id),
            )
            return {"successfully_parsed": False, "all_rooms_details": []}
        else:
            return {"successfully_parsed": True, "all_rooms_details": rooms}

    def _extract_rooms_from_mobile_cards(self, room_elements: list[Node]) -> list[Offer]:
        """Extract all rooms from mobile card elements"""
        rooms: list[Offer] = []

        for room_element in room_elements:
            room_name_element = room_element.css_first(".room__title-text")
            if room_name_element:
                room = self._extract_mobile_room_data(room_element, room_name_element)

                # Extract choice data for the room
                choice = self._extract_mobile_choice_data(room_element)
                if choice:
                    room["offer_choices"].append(choice)

                rooms.append(room)

        return rooms

    def _extract_mobile_room_data(self, room_element: Node, room_name_element: Node) -> Offer:
        """Extract complete mobile room data"""
        # Get room name
        room_name = room_name_element.text().strip()

        # Extract booking ID from data-room-id attribute
        booking_id = None
        details_div = room_element.css_first(".room")
        if details_div:
            booking_id = details_div.attributes.get("data-room-id")

        # Get availability - check for special case scarcity
        availability = 10  # Default normal availability - rooms are available unless specified otherwise
        special_case_availability = False
        availability_element = room_element.css_first(".m_hp_rt_room_card__scarcity.js-scarcity")
        if availability_element:
            print("we have availability element")
            availability_text = availability_element.text()
            scarcity_match = re.search(r"Only (\d+)(?: rooms?| room)? left on our site", availability_text)
            if scarcity_match:
                availability = int(scarcity_match.group(1))
                special_case_availability = True
        # Check if it's a partner offer
        is_partner_offer = False
        if details_div:
            class_names = details_div.attributes.get("class", "") or ""
            is_partner_offer = "js-wholesalers-room-rate" in class_names

        return Offer(
            offer_room_name=room_name,
            offer_booking_id=booking_id,
            offer_availability=availability,
            offer_is_sold_out=False,
            offer_is_partner_offer=is_partner_offer,
            offer_special_case_availability=special_case_availability,
            offer_choices=[],
        )

    def _extract_mobile_choice_data(self, room_element: Node) -> BookingChoice | None:
        """Extract complete booking choice data for mobile"""
        # Get sleeps count from data-max-persons attribute
        sleeps = None
        details_div = room_element.css_first(".room")
        if details_div:
            sleeps_attr = details_div.attributes.get("data-max-persons")
            if sleeps_attr:
                try:
                    sleeps = int(sleeps_attr)
                except ValueError:
                    sleeps = None

        # Get price
        price = self._extract_mobile_price(room_element)
        if price is None:
            return None

        # Get other choice properties
        has_member_discount = self._extract_mobile_member_discount(room_element)
        has_mobile_discount = self._extract_mobile_discount(room_element)
        meal_type = self._extract_mobile_meal_type(room_element)
        non_refundable = self._extract_mobile_non_refundable(room_element)
        no_prepayment_needed = self._extract_mobile_no_prepayment_needed(room_element)
        is_partner_offer = self._extract_mobile_is_partner_offer(room_element)

        return BookingChoice(
            choice_sleeps=sleeps,
            choice_price=price,
            choice_has_member_discount=has_member_discount or has_mobile_discount,
            choice_meal_type=meal_type,
            choice_non_refundable=non_refundable,
            choice_no_prepayment_needed=no_prepayment_needed,
            choice_is_partner_offer=is_partner_offer,
        )

    def _extract_mobile_price(self, room_element: Node) -> float | None:
        """Extract price from mobile room element"""
        price_span = room_element.css_first(".bui-price-display__value")
        if not price_span:
            return None

        price_text = price_span.text().replace("\n", "").replace("\r", "")
        price_match = re.search(r"(\d+,?\d+)(?!.*\d)", price_text)
        if not price_match:
            return None

        try:
            price = float(price_match.group(1).replace(",", ""))

            # Calculate per night price
            nights = cast(int, self.task.task__parsing_price_variables_nights)
            return round(price / nights, 0)

        except (ValueError, TypeError):
            return None

    def _extract_mobile_member_discount(self, room_element: Node) -> bool:
        """Extract member discount status from mobile element"""
        genius_div = room_element.css_first(".m-badge__genius")
        return genius_div is not None

    def _extract_mobile_discount(self, room_element: Node) -> bool:
        """Extract mobile-only discount status"""
        mobile_rate_div = room_element.css_first('[data-component="deals-container"]')
        if mobile_rate_div:
            text = mobile_rate_div.text().strip().lower()
            return "mobile-only price" in text
        return False

    def _extract_mobile_meal_type(self, room_element: Node) -> str:
        """Extract meal type from mobile conditions"""
        conditions_div = room_element.css_first(".bui-list")
        if not conditions_div:
            return "NONE"

        conditions = conditions_div.css("li")
        for condition_li in conditions:
            text = condition_li.text().strip().lower()

            if "breakfast, lunch & dinner included" in text:
                return "FULL_BOARD"
            if "breakfast & dinner included" in text:
                return "HALF_BOARD"
            if "all-inclusive" in text:
                return "ALL_INCLUSIVE"
            if "included" in text and "breakfast" in text:
                return "BREAKFAST"

        return "NONE"

    def _extract_mobile_non_refundable(self, room_element: Node) -> bool:
        """Extract non-refundable status from mobile conditions"""
        conditions_div = room_element.css_first(".bui-list")
        if not conditions_div:
            return False

        conditions = conditions_div.css("li")
        for condition_li in conditions:
            text = condition_li.text().strip().lower()
            if "non-refundable" in text:
                return True
        return False

    def _extract_mobile_no_prepayment_needed(self, room_element: Node) -> bool:
        """Extract no prepayment needed status from mobile conditions"""
        conditions_div = room_element.css_first(".bui-list")
        if not conditions_div:
            return False

        conditions = conditions_div.css("li")
        for condition_li in conditions:
            text = condition_li.text().strip().lower()
            if "no prepayment needed" in text:
                return True
        return False

    def _extract_mobile_is_partner_offer(self, room_element: Node) -> bool:
        """Extract partner offer status from mobile element"""
        details_div = room_element.css_first(".room")
        if details_div:
            class_names = details_div.attributes.get("class", "") or ""
            return "js-wholesalers-room-rate" in class_names
        return False
