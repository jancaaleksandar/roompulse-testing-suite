from typing import TypedDict, Optional, Dict, List

class RoomInfo(TypedDict):
    name: str
    booking_id: str

class HotelInfo(TypedDict, total=False):
    hotel_internal_id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    city: Optional[str]
    address: Optional[str]
    coordinates: Optional[Dict[str, float]]
    rating: Optional[int]
    rating_type: Optional[str]
    preferred_partner: bool
    preferred_partner_plus: bool
    review_score: Optional[str]
    facilities: List[str]
    checkin_time: Optional[str]
    checkout_time: Optional[str]
    highlights: List[str]
    image_url: Optional[str]
    csrf: Optional[str]
    rooms: List[RoomInfo]