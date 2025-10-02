from datetime import datetime, UTC
from typing import List, cast
from hotel_info_lib import ProcessRequestParsingTask, RawHotelInfoCreate, DataProvider
from ..types.hotel import HotelInfo

def booking_raw_hotel_info_mapper(hotel_info: HotelInfo, task: ProcessRequestParsingTask, url: str) -> List[RawHotelInfoCreate]:
    raw_hotel_info_list: List[RawHotelInfoCreate] = []
    
    # Handle coordinates safely
    coordinates = hotel_info.get('coordinates')
    lat = coordinates['latitude'] if coordinates else None
    lng = coordinates['longitude'] if coordinates else None
    
    rooms = hotel_info.get('rooms')
    if not rooms:
        raise ValueError("No rooms found in hotel info")
    for room in rooms:    
        raw_hotel_info_object = RawHotelInfoCreate(
            raw_process_request_id=cast(int, task.task_request_id),
            raw_task_id=cast(int, task.task_id),
            raw_hotel_id=cast(int, task.task_hotel_id),
            raw_hotel_internal_id=cast(str, task.task_hotel_id),
            raw_data_proxy="eu_pool",
            raw_data_provider=DataProvider.BOOKING,
            raw_creation_date=datetime.now(tz=UTC),
            raw_name=room['name'],
            raw_is_preferred_partner=hotel_info.get('preferred_partner', False),
            raw_is_preferred_partner_plus=hotel_info.get('preferred_partner_plus', False),
            raw_check_in_time=hotel_info.get('checkin_time'),
            raw_check_out_time=hotel_info.get('checkout_time'),
            raw_image_url=hotel_info.get('image_url'),
            raw_rating=hotel_info.get('rating'),
            raw_coordinates_lat=lat,
            raw_coordinates_lng=lng,
            raw_city=hotel_info.get('city'),
            raw_type=hotel_info.get('type'),
            raw_address=hotel_info.get('address'),
            raw_csrf=hotel_info.get('csrf'),
            raw_highlights=hotel_info.get('highlights'),
            raw_facilities=hotel_info.get('facilities'),
            raw_rooms=None,  # Not extracted yet
            raw_review_score=hotel_info.get('review_score'),
            raw_rating_type=hotel_info.get('rating_type')
        )
        raw_hotel_info_list.append(raw_hotel_info_object)
    
    return raw_hotel_info_list