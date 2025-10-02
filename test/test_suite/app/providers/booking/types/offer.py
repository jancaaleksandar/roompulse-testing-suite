from typing import TypedDict, Optional, List

class BookingChoice(TypedDict):
    choice_sleeps: Optional[int]
    choice_price: Optional[float]
    choice_has_member_discount: bool
    choice_meal_type: str
    choice_non_refundable: bool
    choice_no_prepayment_needed: bool
    choice_is_partner_offer: bool

class Offer(TypedDict):
    offer_room_name: str
    offer_booking_id: Optional[str]
    offer_availability: int
    offer_is_sold_out: bool
    offer_is_partner_offer: bool
    offer_special_case_availability: bool
    offer_choices: List[BookingChoice]