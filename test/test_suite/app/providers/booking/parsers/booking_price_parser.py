import re
from typing import Any, cast

from hotel_info_lib import ProcessRequestParsingTask, log
from selectolax.parser import HTMLParser, Node

from ..types.offer import BookingChoice, Offer


class BookingPriceParser:
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
                    log_path="app/booking_parser.py | parse",
                    individual_id=cast(int, self.task.task_id),
                )

            # Look for main table
            table = doc.css_first("#hprt-table")

            if table:
                tbody = table.css_first("tbody")
                if tbody:
                    room_elements = tbody.css("tr")
                    if room_elements:
                        rooms = self._extract_rooms_from_table(room_elements)
            else:
                # Check for sold out rooms
                rooms = self._extract_sold_out_rooms(doc)

        except (ValueError, KeyError, AttributeError, TypeError) as e:
            log(
                log_message=f"Parsing failed: {e!s}",
                log_path="app/booking_parser.py | parse",
                individual_id=cast(int, self.task.task_id),
            )
            return {"successfully_parsed": False, "all_rooms_details": []}
        else:
            return {"successfully_parsed": True, "all_rooms_details": rooms}

    def _extract_rooms_from_table(self, room_elements: list[Node]) -> list[Offer]:
        """Extract all rooms from table elements"""
        rooms: list[Offer] = []
        current_room: Offer | None = None

        for room_element in room_elements:
            room_name_element = room_element.css_first(".hprt-roomtype-link")
            if room_name_element:
                # New room found - create with complete data
                current_room = self._extract_room_data(room_element, room_name_element)
                rooms.append(current_room)

            if current_room:
                # Extract choice data for current room
                choice = self._extract_choice_data(room_element)
                if choice:
                    current_room["offer_choices"].append(choice)

        return rooms

    def _extract_sold_out_rooms(self, doc: HTMLParser) -> list[Offer]:
        """Extract sold out rooms"""
        rooms: list[Offer] = []
        maxotel_area = doc.css_first("#maxotelRoomArea")
        if maxotel_area:
            section = maxotel_area.css_first(".roomstable")
            if section:
                room_elements = section.css("> *")  # Direct children
                for room_element in room_elements:
                    link = room_element.css_first("a")
                    if link:
                        room = self._extract_sold_out_room_data(link)
                        rooms.append(room)
        return rooms

    def _extract_room_data(self, room_element: Node, room_name_element: Node) -> Offer:
        """Extract complete room data"""
        # Get room name
        room_name_child = room_name_element.css_first("*")
        room_name = (room_name_child.text() if room_name_child else room_name_element.text()).strip()

        # Extract booking ID from href
        booking_id = None
        href = room_name_element.attributes.get("href", "")
        if href:
            booking_id_match = re.search(r"(\d+)(?!.*\d)", href)
            if booking_id_match:
                booking_id = booking_id_match.group(1)

        # Get availability
        availability = 0
        select_rooms = room_element.css_first(".hprt-nos-select")
        if select_rooms:
            print("we got selected rooms")
            options = select_rooms.css("option")
            availability = max(0, len(options) - 1)  # Subtract 1 for default option

        return Offer(
            offer_room_name=room_name,
            offer_booking_id=booking_id,
            offer_availability=availability,
            offer_is_sold_out=availability == 0,
            offer_is_partner_offer=False,
            offer_special_case_availability=False,
            offer_choices=[],
        )

    def _extract_sold_out_room_data(self, link: Node) -> Offer:
        """Extract sold out room data"""
        # Get room name
        room_name_child = link.css_first("*")
        room_name = (room_name_child.text() if room_name_child else link.text()).strip()

        # Extract booking ID
        booking_id = None
        href = link.attributes.get("href", "")
        if href:
            booking_id_match = re.search(r"(\d+)(?!.*\d)", href)
            if booking_id_match:
                booking_id = booking_id_match.group(1)

        return Offer(
            offer_room_name=room_name,
            offer_booking_id=booking_id,
            offer_availability=0,
            offer_is_sold_out=True,
            offer_is_partner_offer=False,
            offer_special_case_availability=False,
            offer_choices=[],
        )

    def _extract_choice_data(self, room_element: Node) -> BookingChoice | None:
        """Extract complete booking choice data"""
        # Get sleeps count
        sleeps = self._extract_sleeps_count(room_element)
        if not sleeps:
            return None

        # Get price
        price = self._extract_price(room_element)

        # Get other choice properties
        has_member_discount = self._extract_member_discount(room_element)
        meal_type = self._extract_meal_type(room_element)
        non_refundable = self._extract_non_refundable(room_element)
        no_prepayment_needed = self._extract_no_prepayment_needed(room_element)
        is_partner_offer = self._extract_is_partner_offer(room_element)

        return BookingChoice(
            choice_sleeps=sleeps,
            choice_price=price,
            choice_has_member_discount=has_member_discount,
            choice_meal_type=meal_type,
            choice_non_refundable=non_refundable,
            choice_no_prepayment_needed=no_prepayment_needed,
            choice_is_partner_offer=is_partner_offer,
        )

    def _extract_sleeps_count(self, room_element: Node) -> int | None:
        """Extract sleeps count from room element"""
        sleeps_element = room_element.css_first(".c-occupancy-icons__adults")

        if not sleeps_element:
            sleeps_element = room_element.css_first(".wholesalers_table__occupancy__icons")
            if sleeps_element:
                return len(sleeps_element.css("i"))
        else:
            sleeps = len(sleeps_element.css("i"))
            if sleeps == 1:
                # Check for multiplier
                multiplier = sleeps_element.css_first(".c-occupancy-icons__multiplier-number")
                if multiplier:
                    try:
                        sleeps *= int(multiplier.text())
                    except ValueError:
                        pass
            return sleeps
        return None

    def _extract_price(self, room_element: Node) -> float | None:
        """Extract price from room element"""
        price_td = room_element.css_first(".hprt-table-cell-price")
        if not price_td:
            return None

        price_span = price_td.css_first(".bui-u-sr-only")
        if not price_span:
            return None

        price_text = price_span.text().replace("\n", "").replace("\r", "")
        price_match = re.search(r"(\d+,?\d+)(?!.*\d)", price_text)
        if not price_match:
            return None

        try:
            price = float(price_match.group(1).replace(",", ""))

            # Add additional fees
            additional_price_div = price_td.css_first(".prd-taxes-and-fees-under-price")
            if additional_price_div:
                additional_text = additional_price_div.text().replace("\n", "").replace("\r", "")
                additional_match = re.search(r"\b(\d+)\b", additional_text)
                if additional_match:
                    price += float(additional_match.group(1).replace(",", ""))

            # Add excluded taxes (percentage)
            excluded_tax_div = price_td.css_first(".js-us-excluded-fees")
            if excluded_tax_div:
                excluded_text = excluded_tax_div.text().replace("\n", "").replace("\r", "")
                percentage_matches = re.findall(r"(\d+(?:\.\d+)?)\s*%", excluded_text)
                total_percentage = sum(float(match) for match in percentage_matches)
                if total_percentage > 0:
                    price = price * (1 + total_percentage / 100)

            # Calculate per night price
            nights = cast(int, self.task.task__parsing_price_variables_nights)
            return round(price / nights, 0)

        except (ValueError, TypeError):
            return None

    def _extract_member_discount(self, room_element: Node) -> bool:
        """Extract member discount status"""
        genius_div = room_element.css_first(".m-badge__genius")
        return genius_div is not None

    def _extract_meal_type(self, room_element: Node) -> str:
        """Extract meal type from conditions"""
        conditions_div = room_element.css_first(".hprt-conditions-bui")
        if not conditions_div:
            conditions_div = room_element.css_first(".hprt-conditions")

        if conditions_div:
            conditions = conditions_div.css("li")
            for condition_li in conditions:
                text = condition_li.text().strip().lower()

                if "included" in text and "breakfast" in text:
                    return "BREAKFAST"
                if "breakfast & dinner included" in text:
                    return "HALF_BOARD"
                if "breakfast, lunch & dinner included" in text:
                    return "FULL_BOARD"
                if "all-inclusive" in text:
                    return "ALL_INCLUSIVE"
        return "NONE"

    def _extract_non_refundable(self, room_element: Node) -> bool:
        """Extract non-refundable status"""
        conditions_div = room_element.css_first(".hprt-conditions-bui")
        if not conditions_div:
            conditions_div = room_element.css_first(".hprt-conditions")

        if conditions_div:
            conditions = conditions_div.css("li")
            for condition_li in conditions:
                text = condition_li.text().strip().lower()
                if "non-refundable" in text:
                    return True
        return False

    def _extract_no_prepayment_needed(self, room_element: Node) -> bool:
        """Extract no prepayment needed status"""
        conditions_div = room_element.css_first(".hprt-conditions-bui")
        if not conditions_div:
            conditions_div = room_element.css_first(".hprt-conditions")

        if conditions_div:
            conditions = conditions_div.css("li")
            for condition_li in conditions:
                text = condition_li.text().strip().lower()
                if "no prepayment needed" in text:
                    return True
        return False

    def _extract_is_partner_offer(self, room_element: Node) -> bool:
        """Extract partner offer status"""
        sleeps_element = room_element.css_first(".wholesalers_table__occupancy__icons")
        return sleeps_element is not None
