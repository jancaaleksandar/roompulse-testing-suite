from datetime import datetime
from typing import cast, Dict, TypedDict
from hotel_info_lib import ProcessRequestParsingTask
from hotel_info_lib.common.common_datetime_to_date import datetime_to_date
from hotel_info_lib.common.common_calculate_check_out_date import calculate_check_out_date
from .utils.get_booking_cookie import get_booking_cookie

class BookingConfig(TypedDict):
    url : str
    headers : Dict[str, str]
    cookie : str

def get_booking_config(task: ProcessRequestParsingTask) -> BookingConfig:
    base_url = "https://www.booking.com"
    if str(task.task__parsing_variables_platform) == "MOBILE":
        base_url = "https://m.booking.com"
    
    check_in_date = datetime_to_date(cast(datetime, task.task__parsing_start_date))
    check_out_date_datetime = calculate_check_out_date(start_date=cast(datetime, task.task__parsing_start_date), number_of_nights=cast(int, task.task__parsing_price_variables_nights))
    check_out_date = datetime_to_date(check_out_date_datetime)
    url = f"{base_url}/hotel/{task.task_hotel_provider_id}.en-gb.html?checkin={check_in_date}&checkout={check_out_date}&dist=0&group_adults={task.task__parsing_price_variables_guests}&group_children=0&hapos=1&req_adults={task.task__parsing_price_variables_guests}&req_children=0&selected_currency={task.task__parsing_price_variables_currency}"
    
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    }
    
    cookie = get_booking_cookie(task=task)
    
    return BookingConfig(url=url, headers=headers, cookie=cookie)