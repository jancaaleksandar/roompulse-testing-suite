from datetime import datetime
from typing import TypedDict, cast
from ...types import UserInput
from hotel_info_lib.common.common_calculate_check_out_date import calculate_check_out_date
from hotel_info_lib.common.common_datetime_to_date import datetime_to_date

from .utils.get_booking_cookie import get_booking_cookie


class BookingConfig(TypedDict):
    url: str
    headers: dict[str, str]
    cookie: str


def get_booking_config(params: UserInput) -> BookingConfig:
    currency = params.get("request_currency")
    if currency is None:
        raise ValueError("request_currency is none")
    base_url = "https://www.booking.com"
    # if str(params) == "MOBILE":
    #     base_url = "https://m.booking.com"
    check_out_date_datetime = calculate_check_out_date(
        start_date=cast(datetime, params["request_check_in_date"]), number_of_nights=params["request_nights"]
    )
    check_out_date = datetime_to_date(check_out_date_datetime)
    url = f"{base_url}/hotel/{params['provider_id']}.en-gb.html?checkin={params['request_check_in_date']}&checkout={check_out_date}&dist=0&group_adults={params['request_adults']}&group_children=0&hapos=1&req_adults={params['request_adults']}&req_children=0&selected_currency={currency}"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-GB,en;q=0.7",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
    }

    cookie = get_booking_cookie()

    return BookingConfig(url=url, headers=headers, cookie=cookie)
