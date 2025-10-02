import json
import re
from typing import TypedDict, cast

from hotel_info_lib import ProcessRequestParsingTask, log
from selectolax.parser import HTMLParser

from ..types.hotel import HotelInfo, RoomInfo


class CheckingTimes(TypedDict):
    check_in_time: str | None
    check_out_time: str | None


class RatingText(TypedDict):
    rating_type: str
    rating_rating: int


class ReviewScore(TypedDict):
    review_count: int
    average_rating: float
    breakdown: dict[str, float]


class HotelInfoParserResponse(TypedDict):
    successfully_parsed: bool
    hotel_info: HotelInfo


class BookingHotelInfoParser:
    def __init__(self, response: str, task: ProcessRequestParsingTask) -> None:
        self.response = response
        self.task = task
        self.doc = HTMLParser(self.response)

    def parse(self) -> HotelInfoParserResponse:
        successfully_parsed = False
        hotel_info: HotelInfo = {}
        try:
            rating = self._find_hotel_rating()
            hotel_info = HotelInfo(
                hotel_internal_id=self._find_hotel_internal_id(),
                name=self._find_name(),
                type=self._find_type(),
                city=self._find_city(),
                address=self._find_address(),
                coordinates=self._find_coordinates(),
                rating=rating["rating_rating"],
                rating_type=rating["rating_type"],
                preferred_partner=self._find_preferred_partner(),
                preferred_partner_plus=self._find_preferred_partner_plus(),
                review_score=self._find_review_scores(),
                facilities=self._find_most_popular_facilities(),
                highlights=self._find_highlights(),
                image_url=self._find_main_image_url(),
                csrf=self._find_csrf(),
                rooms=self._find_rooms(),
            )

            successfully_parsed = True

        except (ValueError, KeyError, AttributeError, TypeError) as e:
            log(
                log_message=f"Hotel info parsing failed: {e!s}",
                log_path="app/parsers/booking_hotel_info_parser.py | parse",
                individual_id=cast(int, self.task.task_id),
            )
            successfully_parsed = False

        return HotelInfoParserResponse(successfully_parsed=successfully_parsed, hotel_info=hotel_info)

    def _find_hotel_internal_id(self) -> str | None:
        """Extract hotel ID from JavaScript in HTML"""
        pattern = re.compile(r"hotel_id: '(.*?)'")
        match = pattern.search(self.response)
        if match:
            return match.group(1)
        else:
            return None

    def _find_hotel_rating(self) -> RatingText:
        """Find hotel rating (stars/circles/squares)"""
        rating_type = "UNDEFINED"
        rating_rating = 0
        elements = self.doc.css('[data-testid="quality-rating"]')
        if elements:
            element = elements[0]
            children = element.css("*")
            if children:
                child = children[0]
                data_testid = child.attributes.get("data-testid", "")

                if data_testid == "rating-stars":
                    rating_type = "STARS"
                elif data_testid == "rating-circles":
                    rating_type = "CIRCLES"
                elif data_testid == "rating-squares":
                    rating_type = "SQUARES"
                else:
                    rating_type = "OTHER"

                # Count rating elements (stars/circles/squares)
                rating_elements = child.css("*")
                rating_rating = len(rating_elements) if rating_elements else 0

        return RatingText(rating_type=rating_type, rating_rating=rating_rating)

    def _find_name(self) -> str | None:
        """Find hotel name"""
        name_div = self.doc.css_first("#hp_hotel_name")
        if name_div:
            title_div = name_div.css_first(".pp-header__title")
            if title_div:
                return title_div.text()
        else:
            return None

    def _find_type(self) -> str | None:
        """Find hotel type from JavaScript"""
        pattern = re.compile(r"atnm_en: '(.*)'")
        match = pattern.search(self.response)
        if match:
            return match.group(1)
        else:
            return None

    def _find_city(self) -> str | None:
        """Find city from JavaScript"""
        pattern = re.compile(r"city_name: '(.*)'")
        match = pattern.search(self.response)
        if match:
            return match.group(1)
        else:
            return None

    def _find_address(self) -> str | None:
        """Find address from JSON-LD or JavaScript"""
        pattern = re.compile(r'"?addressLocality"?.*?: "(.*?)"')
        match = pattern.search(self.response)
        if match:
            return match.group(1)
        else:
            return None

    def _find_coordinates(self) -> dict[str, float] | None:
        """Find coordinates from data-atlas-latlng attribute"""
        pattern = re.compile(r'"?data-atlas-latlng"?.*?="(.*?)"')
        match = pattern.search(self.response)
        if match:
            latlng = match.group(1)
            if latlng and "," in latlng:
                try:
                    lat, lng = latlng.split(",")
                    return {"latitude": float(lat.strip()), "longitude": float(lng.strip())}
                except (ValueError, IndexError):
                    return None
            else:
                return None
        else:
            return None

    def _find_preferred_partner(self) -> bool:
        """Find preferred partner status"""
        title_div = self.doc.css_first("div.hp__hotel-title")
        if title_div:
            # Check for preferred partner
            thumbs_up = title_div.css_first("svg.-iconset-thumbs_up_square")
            return thumbs_up is not None
        return False

    def _find_preferred_partner_plus(self) -> bool:
        """Find preferred partner plus status"""
        title_div = self.doc.css_first("div.hp__hotel-title")
        if title_div:
            # Check for preferred partner plus
            plus_img = title_div.css_first("img[data-et-mouseenter]")
            return plus_img is not None
        return False

    def _find_review_scores(self) -> str | None:
        """Find review scores and detailed breakdown"""
        # Find overall review score
        review_count_pattern = re.compile(r'"?reviewCount"?.*?: (.*?),')
        rating_pattern = re.compile(r'"?ratingValue"?.*?: (.*?),')

        review_count_match = review_count_pattern.search(self.response)
        rating_match = rating_pattern.search(self.response)

        if review_count_match and rating_match:
            try:
                review_count = int(review_count_match.group(1))
                rating_value = float(rating_match.group(1))

                review_score: ReviewScore = {
                    "review_count": review_count,
                    "average_rating": rating_value,
                    "breakdown": {},
                }
                return str(review_score["average_rating"])

            except (ValueError, TypeError):
                pass

    # def _find_review_breakdown(self) -> None:
    #     """Find detailed review score breakdown"""
    #     review_score_data = self.hotel_info.get("review_score")
    #     if not review_score_data or not isinstance(review_score_data, dict):
    #         return

    #     review_score = cast(ReviewScore, review_score_data)

    #     breakdown_list = doc.css_first('.review_score_breakdown_list')
    #     if breakdown_list:
    #         score_names = breakdown_list.css('.review_score_name')
    #         for score_element in score_names:
    #             score_name = score_element.text().lower()

    #             # Find the next sibling with score
    #             next_element = score_element.parent
    #             if next_element:
    #                 score_child = next_element.css_first('[data-score]')
    #                 if score_child:
    #                     try:
    #                         score_attr = score_child.attributes.get('data-score', '0')
    #                         if score_attr:
    #                             score_value = float(score_attr)

    #                             if 'cleanliness' in score_name:
    #                                 review_score["breakdown"]["cleanliness"] = score_value
    #                             elif 'staff' in score_name:
    #                                 review_score["breakdown"]["staff"] = score_value
    #                             elif 'location' in score_name:
    #                                 review_score["breakdown"]["location"] = score_value
    #                             elif 'value for money' in score_name:
    #                                 review_score["breakdown"]["value_for_money"] = score_value
    #                             elif 'facilities' in score_name:
    #                                 review_score["breakdown"]["facilities"] = score_value
    #                             elif 'free wifi' in score_name:
    #                                 review_score["breakdown"]["wifi"] = score_value

    #                     except (ValueError, TypeError):
    #                         pass

    def _find_most_popular_facilities(self) -> list[str]:
        """Find most popular facilities"""
        facilities: list[str] = []
        facility_elements = self.doc.css(".important_facility")
        for element in facility_elements:
            facility_text = element.text().strip()
            if facility_text:
                facilities.append(facility_text)
        return facilities

    def _find_check_times(self) -> CheckingTimes:
        """Find check-in and check-out times"""
        check_times = CheckingTimes(check_in_time=None, check_out_time=None)
        try:
            time_elements = self.doc.css('[data-component="prc/timebar"]')
            if len(time_elements) >= 2:
                check_in_time = time_elements[0].attributes.get("data-from")
                check_out_time = time_elements[1].attributes.get("data-until")
                check_times = CheckingTimes(check_in_time=check_in_time, check_out_time=check_out_time)
        except (IndexError, AttributeError, KeyError) as e:
            log(
                log_message=f"Error finding check-in and check-out times: {e!s}",
                log_path="app/parsers/booking_hotel_info_parser.py | _find_check_times",
                individual_id=cast(int, self.task.task_id),
            )
            check_times = CheckingTimes(check_in_time=None, check_out_time=None)

        return check_times

    def _find_highlights(self) -> list[str]:
        """Find hotel highlights"""
        highlights: list[str] = []
        highlight_elements = self.doc.css(".facility-badge__tooltip-title")
        for element in highlight_elements:
            highlight_text = element.text().strip()
            if highlight_text:
                highlights.append(highlight_text)
        return highlights

    def _find_main_image_url(self) -> str | None:
        """Find main hotel image URL from og:image meta tag"""
        pattern = re.compile(r'<meta property=["\']og:image["\'] content=["\'](.*)["\']\s*/?>', re.MULTILINE)
        match = pattern.search(self.response)
        if match:
            return match.group(1)
        else:
            return None

    def _find_csrf(self) -> str | None:
        """Find CSRF token"""
        pattern = re.compile(r"'X-Booking-CSRF': '((.*?).*)'")
        match = pattern.search(self.response)
        if match:
            return match.group(1)
        else:
            return None

    def _find_rooms(self) -> list[RoomInfo]:
        """Find rooms from JSON data embedded in HTML or from room links"""
        rooms: list[RoomInfo] = []

        # First try to find JSON data embedded in script tags
        rooms = self._extract_rooms_from_json()
        if rooms:
            return rooms

        # Fallback: extract rooms from HTML room links
        rooms = self._extract_rooms_from_html()
        return rooms

    def _extract_rooms_from_json(self) -> list[RoomInfo]:
        """Extract rooms from JSON data embedded in HTML"""
        rooms: list[RoomInfo] = []
        try:
            # Look for JSON data in script tags
            script_pattern = re.compile(r"<script[^>]*>(.*?)</script>", re.DOTALL)
            scripts = script_pattern.findall(self.response)

            for script_content in scripts:
                if '"roomCards"' in script_content or '"roomTable"' in script_content:
                    # Try to extract JSON from the script
                    json_match = re.search(r'\{.*"roomCards".*\}', script_content, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(0))
                        room_table = data.get("data", {}).get("roomTable", {})
                        rooms_json = room_table.get("roomCards", [])

                        for room_data in rooms_json:
                            name = room_data.get("name", "").strip()
                            room_id = room_data.get("roomId")

                            if name and room_id is not None:
                                rooms.append(RoomInfo(name=name, booking_id=str(room_id)))
                        break

        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            log(
                log_message=f"Could not extract rooms from JSON: {e!s}",
                log_path="app/parsers/booking_hotel_info_parser.py | _extract_rooms_from_json",
                individual_id=cast(int, self.task.task_id),
            )

        return rooms

    def _extract_rooms_from_html(self) -> list[RoomInfo]:
        """Extract rooms from HTML room links as fallback"""
        rooms: list[RoomInfo] = []
        try:
            # Look for room links in the HTML
            room_links = self.doc.css(".hprt-roomtype-link")
            for link in room_links:
                # Get room name
                room_name = link.text().strip() if link.text() else ""

                # Extract room ID from href
                href = link.attributes.get("href", "")
                if href:
                    room_id_match = re.search(r"room_id[=:](\d+)", href)
                    if not room_id_match:
                        # Try different patterns
                        room_id_match = re.search(r"(\d+)(?!.*\d)", href)

                    if room_id_match and room_name:
                        rooms.append(RoomInfo(name=room_name, booking_id=room_id_match.group(1)))

        except (AttributeError, KeyError, IndexError, ValueError) as e:
            log(
                log_message=f"Could not extract rooms from HTML: {e!s}",
                log_path="app/parsers/booking_hotel_info_parser.py | _extract_rooms_from_html",
                individual_id=cast(int, self.task.task_id),
            )

        return rooms
