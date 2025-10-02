
from ....types import UserInput
from typing import TypedDict, Literal

class GoogleConfig(TypedDict):
    url : str
    headers : dict[str, str]
    cookies : dict[str, str]
    type : Literal["GET", "POST"]
    proxy_url : str

def get_google_night_price_config(params : UserInput) -> GoogleConfig:
    url = f"https://www.google.com/maps/place/data=!4m11!3m10!1s{params['provider_id']}!5m4!1s{params['request_check_in_date']}!2i{params['request_nights']}!4m1!1i2!8m2!3d00.0000000!4d00.0000000!16s?ucbcb=1&entry=ttu"
    print("url : ", url)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Google Chrome";v="138", "Chromium";v="138", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }
    proxy_url = params["request_proxy"]
    if proxy_url is None:
        raise ValueError("Proxy URL is required")
    
    return GoogleConfig(url=url, headers=headers, cookies={}, type="GET", proxy_url=proxy_url)