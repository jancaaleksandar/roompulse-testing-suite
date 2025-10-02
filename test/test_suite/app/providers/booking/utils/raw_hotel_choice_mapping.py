from typing import List, cast
from hotel_info_lib import RawHotelChoiceCreate, ProcessRequestParsingTask, DataProvider, DataPlatform, MealEnum
from hotel_info_lib.common import calculate_check_out_date
from hotel_info_lib.logging import log
from ..types.offer import Offer
from datetime import datetime, UTC

def booking_raw_hotel_choice_mapper(all_offers: List[Offer], task: ProcessRequestParsingTask, url: str) -> List[RawHotelChoiceCreate]:
    check_out_date: datetime = calculate_check_out_date(cast(datetime, task.task__parsing_start_date), cast(int, task.task__parsing_price_variables_nights))
    raw_hotel_choice_list: List[RawHotelChoiceCreate] = []
    
    # Iterate through all offers (rooms)
    for offer in all_offers:
        if not offer["offer_choices"]:
            continue
        # Create one entry for each choice
        for choice in offer["offer_choices"]:
            # Map meal type string to enum
            meal_enum = MealEnum.NONE
            meal_type = choice["choice_meal_type"]
            if meal_type == "BREAKFAST":
                meal_enum = MealEnum.BREAKFAST
            elif meal_type == "HALF_BOARD":
                meal_enum = MealEnum.HALF_BOARD
            elif meal_type == "FULL_BOARD":
                meal_enum = MealEnum.FULL_BOARD
            elif meal_type == "ALL_INCLUSIVE":
                meal_enum = MealEnum.ALL_INCLUSIVE
            
            raw_hotel_choice_object = RawHotelChoiceCreate(
                raw_process_request_id=cast(int, task.task_request_id),
                raw_task_id=cast(int, task.task_id),
                raw_hotel_id=cast(int, task.task_hotel_id),
                raw_hotel_name="",
                raw_region=cast(str, task.task__parsing_variables_region),
                raw_data_provider=DataProvider.BOOKING,
                raw_data_platform=cast(DataPlatform, task.task__parsing_variables_platform),
                raw_data_proxy="eu_pool",
                raw_availability=offer["offer_availability"],
                raw_creation_date=datetime.now(tz=UTC),
                raw_parse_date=datetime.now(tz=UTC).date(),
                raw_check_in_date=cast(datetime, task.task__parsing_start_date),
                raw_check_out_date=check_out_date,
                raw_is_last_minute_enabled=False,
                raw_room_name=offer["offer_room_name"],
                raw_room_is_sold_out=offer["offer_is_sold_out"],
                raw_sleeps=choice["choice_sleeps"],
                raw_price_amount=choice["choice_price"],
                raw_price_currency=cast(str, task.task__parsing_price_variables_currency),
                raw_meal=meal_enum,
                raw_non_refundable=choice["choice_non_refundable"],
                raw_has_member_discount=choice["choice_has_member_discount"],
                raw_has_mobile_discount=False,
                raw_is_partner_offer=choice["choice_is_partner_offer"] or offer["offer_is_partner_offer"],
                raw_url=url,
                raw_filter_key=cast(str, task.task__parsing_filter_key),
                raw_filter_los_key=cast(str, task.task__parsing_filter_los_key),
            )
            raw_hotel_choice_list.append(raw_hotel_choice_object)
    
    # Log summary
    total_choices = sum(len(offer["offer_choices"]) for offer in all_offers)
    log(
        log_path="raw_hotel_choice_mapper.py",
        log_message=f"Created {len(raw_hotel_choice_list)} hotel choices from {len(all_offers)} rooms with {total_choices} total booking choices",
        log_level="INFO"
    )
    
    return raw_hotel_choice_list