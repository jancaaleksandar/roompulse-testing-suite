from typing import Any

from hotel_info_lib import Request, RequestParameters

from ...types import UserInput
from .booking_config import get_booking_config


def booking_request(params: UserInput) -> dict[str, Any]:
    successfully_scraped = False
    scraped_data = None
    url = None
    try:
        config = get_booking_config(params)

        # Parse cookie string into dictionary format
        cookie_str = config["cookie"]
        cookies_dict: dict[str, str] = {}
        if cookie_str:
            # Extract the first key=value pair before any semicolon
            cookie_part = cookie_str.split(";")[0]
            if "=" in cookie_part:
                key, value = cookie_part.split("=", 1)
                cookies_dict[key] = value

        request_params = RequestParameters(
            url=config["url"],
            request_headers=config["headers"],
            request_type="GET",
            request_params={},
            request_cookies=cookies_dict,
        )

        request = Request(params=request_params)

        response = request.curl_request_api_get()

        if not response:
            raise (ValueError)("Request failed")
        else:
            successfully_scraped = True
            scraped_data = response
            url = config["url"]
    except (ValueError, AttributeError, TypeError, KeyError) as e:
        successfully_scraped = False
        print(f"Error scraping booking.com: {e}")

    return {"successfully_scraped": successfully_scraped, "scraped_data": {"url": url, "data": scraped_data}}
