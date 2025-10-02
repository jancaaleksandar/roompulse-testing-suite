from collections.abc import Mapping
from datetime import datetime
import re

from hotel_info_lib import ProcessRequestParsingTask, log
from selectolax.parser import HTMLParser, Node

from ..types.promotion import PromotionDealWithChoice


class BookingHotelPromotionsParser:
    def __init__(self, html_content: str, task: ProcessRequestParsingTask):
        self.html_content = html_content
        self.task = task
        # Handle task_id properly - convert to int if it exists, otherwise use 0
        task_id_val = getattr(task, "task_id", None)
        self.individual_id = int(task_id_val) if task_id_val is not None else 0
        self.promotion_id = getattr(task, "hotel_id", "") or ""
        # Get check-in date from task parameters
        self.checkin_date_str = getattr(task, "check_in_date", None) or "2024-01-01"
        # Initialize selectolax parser
        self.parser = HTMLParser(html_content)

    # --- Helper Parsing Methods ---

    def _parse_preferred_deal(self, hotel_page_top_block: Node) -> bool:
        """Check for preferred icon in hotel top block."""
        preferred_icon = hotel_page_top_block.css_first('span[data-testid="preferred-icon"]')
        return preferred_icon is not None

    def _parse_preferred_plus_deal(self, hotel_page_top_block: Node) -> bool:
        """Check for preferred plus icon in hotel top block."""
        preferred_plus_span = hotel_page_top_block.css_first('span[data-testid="preferred-plus-icon"]')
        return preferred_plus_span is not None

    def _parse_basic_deal(self, potential_deal_nodes: list[Node]) -> bool:
        """Check for 'Bonus savings' text in deal nodes."""
        if not potential_deal_nodes:
            return False

        for node in potential_deal_nodes:
            if node.text() and "Bonus savings" in node.text():
                return True
        return False

    def _parse_booking_pays(self, potential_deal_nodes: list[Node]) -> bool:
        """Check for 'Booking.com pays' text in deal nodes."""
        if not potential_deal_nodes:
            return False

        for node in potential_deal_nodes:
            if node.text() and "Booking.com pays" in node.text():
                return True
        return False

    def _parse_new_property_deal(self, room_node: Node) -> bool:
        """Check for 'New Property Deal' badge."""
        badge = room_node.css_first("span.bui-badge__text")
        return badge is not None and badge.text() == "New Property Deal"

    def _parse_getaway_deal(self, room_node: Node) -> bool:
        """Check for 'Getaway Deal' badge."""
        badge = room_node.css_first("span.bui-badge__text")
        return badge is not None and badge.text() == "Getaway Deal"

    def _parse_early_booker_deal(self, potential_deal_nodes: list[Node]) -> bool:
        """Check for 'Early Booker Deal' text in deal nodes."""
        if not potential_deal_nodes:
            return False

        for node in potential_deal_nodes:
            if node.text() and "Early Booker Deal" in node.text():
                return True
        return False

    def _parse_last_minute_deal(self, potential_deal_nodes: list[Node]) -> bool:
        """Check for 'Last-minute Deal' text in deal nodes."""
        if not potential_deal_nodes:
            return False

        for node in potential_deal_nodes:
            if node.text() and "Last-minute Deal" in node.text():
                return True
        return False

    def _parse_limited_time_deal(self, room_node: Node) -> bool:
        """Check for 'Limited Time Deal' badge."""
        badge = room_node.css_first("span.bui-badge__text")
        return badge is not None and badge.text() == "Limited Time Deal"

    def _parse_partner_offer_deal(self, room_node: Node) -> bool:
        """Check for 'Partner offer' badge."""
        badge = room_node.css_first("span.bui-badge__text")
        return badge is not None and badge.text() == "Partner offer"

    def _parse_genius_deal(self, room_node: Node) -> bool:
        """Check for Genius discount."""
        genius_div = room_node.css_first('div[aria-label*="Genius discount"]')
        return genius_div is not None

    def _parse_choice_cancellation(self, policy_nodes: list[Node]) -> Mapping[str, bool | int | None]:
        """Parse cancellation policy information."""
        if not policy_nodes:
            return {"cancellation_free": False, "cancellation_days_difference": None}

        for node in policy_nodes:
            policy_text = node.text() or ""

            if "Free cancellation" in policy_text:
                # Look for date pattern: "before Month Day, Year"
                match = re.search(r"before\s+(\w+)\s+(\d{1,2}),\s+(\d{4})", policy_text, re.IGNORECASE)

                if match:
                    month_str = match.group(1)
                    day_str = match.group(2)
                    year_str = match.group(3)
                    cancellation_date_str = f"{day_str} {month_str} {year_str}"

                    try:
                        cancellation_date = datetime.strptime(cancellation_date_str, "%d %B %Y").date()
                        checkin_date = datetime.strptime(self.checkin_date_str, "%Y-%m-%d").date()
                        day_difference = (checkin_date - cancellation_date).days

                        result = {"cancellation_free": True, "cancellation_days_difference": day_difference}
                    except ValueError:
                        log(
                            log_level="error",
                            log_message=f"Date parsing failed for cancellation policy: {cancellation_date_str}",
                            individual_id=self.individual_id,
                            log_path="app/parsers/booking_hotel_promotions_parser.py | _parse_choice_cancellation",
                        )
                        result = {"cancellation_free": True, "cancellation_days_difference": None}
                else:
                    result = {"cancellation_free": True, "cancellation_days_difference": None}
                return result

        return {"cancellation_free": False, "cancellation_days_difference": None}

    def _parse_choice_pay_nothing(self, policy_nodes: list[Node]) -> Mapping[str, bool | int | None]:
        """Parse 'pay nothing until' policy information."""
        if not policy_nodes:
            return {"pay_nothing_found": False, "pay_nothing_day_difference": None}

        for node in policy_nodes:
            policy_text = node.text() or ""

            if "Pay nothing until" in policy_text:
                # Look for date pattern: "Pay nothing until Month Day, Year"
                match = re.search(r"Pay nothing until\s+(\w+)\s+(\d{1,2}),\s+(\d{4})", policy_text, re.IGNORECASE)

                if match:
                    month_str = match.group(1)
                    day_str = match.group(2)
                    year_str = match.group(3)
                    pay_date_str = f"{day_str} {month_str} {year_str}"

                    try:
                        pay_date = datetime.strptime(pay_date_str, "%d %B %Y").date()
                        checkin_date = datetime.strptime(self.checkin_date_str, "%Y-%m-%d").date()
                        day_difference = (checkin_date - pay_date).days

                        result = {"pay_nothing_found": True, "pay_nothing_day_difference": day_difference}
                    except ValueError:
                        log(
                            log_level="error",
                            log_message=f"Date parsing failed for pay nothing policy: {pay_date_str}",
                            individual_id=self.individual_id,
                            log_path="app/parsers/booking_hotel_promotions_parser.py | _parse_choice_pay_nothing",
                        )
                        result = {"pay_nothing_found": True, "pay_nothing_day_difference": None}
                else:
                    result = {"pay_nothing_found": True, "pay_nothing_day_difference": None}
                return result

        return {"pay_nothing_found": False, "pay_nothing_day_difference": None}

    def _parse_airport_shuttle_deal(self) -> bool:
        """Check for airport shuttle deal."""
        promotion_div = self.parser.css_first('div[data-testid="PropertyTripPromotionsBadge-wrapper"]')
        if promotion_div and promotion_div.text():
            return "free taxi" in promotion_div.text().lower()
        return False

    def _extract_promotion_id(self, room_node: Node) -> str | None:
        """Try to extract promotion ID from room node attributes or data."""
        # Look for data attributes that might contain promotion ID
        promotion_attrs = ["data-promotion-id", "data-deal-id", "data-offer-id"]

        for attr in promotion_attrs:
            value = room_node.attributes.get(attr)
            if value:
                return value

        # Look for promotion ID in nested elements
        promo_elements = room_node.css("*[data-promotion-id], *[data-deal-id], *[data-offer-id]")
        for element in promo_elements:
            for attr in promotion_attrs:
                value = element.attributes.get(attr)
                if value:
                    return value

        return None

    def parse(self) -> Mapping[str, bool | list[PromotionDealWithChoice]]:
        """Main parsing method."""
        successfully_parsed = False
        deals: list[PromotionDealWithChoice] = []
        unique_cancellation_day_options: set[int] = set()
        unique_pay_nothing_day_options: set[int] = set()
        sold_out = False

        try:
            # Check for sold out status
            no_availability_span = self.parser.css_first("span.bui-alert__title")
            if no_availability_span and "We have no availability" in (no_availability_span.text() or ""):
                sold_out = True

            if not sold_out:
                sold_out_paragraph = self.parser.css_first("p.bui-alert__text")
                if sold_out_paragraph and "Select different dates to see more availability" in (
                    sold_out_paragraph.text() or ""
                ):
                    sold_out = True

            if not sold_out:
                # Main parsing logic
                hotel_page_top_block = self.parser.css_first("div.wrap-hotelpage-top")
                if not hotel_page_top_block:
                    raise ValueError("hotel_page_top_block was not found (and page not flagged as sold out).")

                preferred_deal = self._parse_preferred_deal(hotel_page_top_block)
                preferred_plus_deal = self._parse_preferred_plus_deal(hotel_page_top_block)

                room_data_block = self.parser.css_first("div#available_rooms")
                if not room_data_block:
                    log(
                        log_level="warn",
                        log_message="room_data_block not found, though page not initially flagged as sold out",
                        individual_id=self.individual_id,
                        log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                    )
                else:
                    room_data_table = room_data_block.css_first("table#hprt-table")
                    if not room_data_table:
                        log(
                            log_level="info",
                            log_message="room_data_table not found. No deals will be parsed from table",
                            individual_id=self.individual_id,
                            log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                        )
                    else:
                        table_body = room_data_table.css_first("tbody")
                        if not table_body:
                            log(
                                log_level="info",
                                log_message="tbody not found within hprt-table. No deals will be parsed from table",
                                individual_id=self.individual_id,
                                log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                            )
                        else:
                            all_potential_room_rows = table_body.css("tr")
                            if not all_potential_room_rows:
                                raise ValueError(
                                    "No tr elements (room rows) found within tbody. No deals parsed from table."
                                )
                            else:
                                log(
                                    log_level="info",
                                    log_message=f"Found {len(all_potential_room_rows)} potential room rows to process",
                                    individual_id=self.individual_id,
                                    log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                                )

                                for room_tr in all_potential_room_rows:
                                    potential_deal_nodes = room_tr.css("div.bui-f-font-body")
                                    policy_nodes = room_tr.css('div[data-testid="policy-subtitle"]')

                                    if not policy_nodes:
                                        log(
                                            log_level="warn",
                                            log_message="No policy nodes found within a specific room_tr",
                                            individual_id=self.individual_id,
                                            log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                                        )

                                    # Parse cancellation information
                                    cancellation_info = self._parse_choice_cancellation(policy_nodes)
                                    cancellation_free = bool(cancellation_info["cancellation_free"])
                                    cancellation_days_val = cancellation_info["cancellation_days_difference"]
                                    current_deal_cancellation_days_list = (
                                        [cancellation_days_val] if cancellation_days_val is not None else []
                                    )

                                    if cancellation_days_val is not None:
                                        unique_cancellation_day_options.add(cancellation_days_val)

                                    # Parse pay nothing information
                                    pay_nothing_info = self._parse_choice_pay_nothing(policy_nodes)
                                    pay_nothing_found = bool(pay_nothing_info["pay_nothing_found"])
                                    pay_nothing_day_diff_val = pay_nothing_info["pay_nothing_day_difference"]

                                    current_deal_pay_nothing_days_list: list[int] = []
                                    if pay_nothing_day_diff_val is not None:
                                        current_deal_pay_nothing_days_list.append(pay_nothing_day_diff_val)
                                        unique_pay_nothing_day_options.add(pay_nothing_day_diff_val)

                                    # Extract promotion ID
                                    promotion_id = self._extract_promotion_id(room_tr)

                                    # Create deal info with new types
                                    deal_info = PromotionDealWithChoice(
                                        promotion_deal_preferred=preferred_deal,
                                        promotion_deal_preferred_plus=preferred_plus_deal,
                                        promotion_deal_basic=self._parse_basic_deal(potential_deal_nodes),
                                        promotion_deal_booking_pays=self._parse_booking_pays(potential_deal_nodes),
                                        promotion_deal_new_property=self._parse_new_property_deal(room_tr),
                                        promotion_deal_getaway=self._parse_getaway_deal(room_tr),
                                        promotion_deal_early_booker=self._parse_early_booker_deal(potential_deal_nodes),
                                        promotion_deal_last_minute=self._parse_last_minute_deal(potential_deal_nodes),
                                        promotion_deal_limited_time=self._parse_limited_time_deal(room_tr),
                                        promotion_deal_partner_offer=self._parse_partner_offer_deal(room_tr),
                                        promotion_deal_genius=self._parse_genius_deal(room_tr),
                                        promotion_deal_promotion_id=promotion_id,
                                        promotion_deal_offer_airport_shuttle=self._parse_airport_shuttle_deal(),
                                        promotion_choice_cancellation_free=cancellation_free,
                                        promotion_choice_cancellation_days=current_deal_cancellation_days_list,
                                        promotion_choice_pay_nothing=pay_nothing_found,
                                        promotion_choice_pay_nothing_days=current_deal_pay_nothing_days_list,
                                    )
                                    deals.append(deal_info)

                log(
                    log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                    log_message=f"Main parsing block completed. Found {len(deals)} deals. Setting successfully_parsed=True.",
                    log_level="info",
                    individual_id=self.individual_id,
                )
                successfully_parsed = True
            else:
                log(
                    log_level="info",
                    log_message="Page identified as sold out. Skipping main deal parsing. successfully_parsed remains False.",
                    individual_id=self.individual_id,
                    log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                )

        except (ValueError, KeyError, AttributeError, TypeError) as e:
            log(
                log_path="app/parsers/booking_hotel_promotions_parser.py | parse",
                log_message=f"Error during parsing process: {e!s}",
                log_level="error",
                individual_id=self.individual_id,
            )
            successfully_parsed = False

        return {"successfully_parsed": successfully_parsed, "deals": deals, "sold_out": sold_out}
