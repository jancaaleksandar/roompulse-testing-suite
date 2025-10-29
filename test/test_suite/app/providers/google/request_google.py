import time
from typing import TypedDict

from curl_cffi.requests.exceptions import ProxyError, Timeout

from ...types import RequestParameters, UserInput
from ...utils.http.request_http import Request
from .config.google_night_price_config import get_google_night_price_config


class GoogleRequestResponse(TypedDict):
    response: str
    response_headers: dict[str, str] | None
    successfully_scraped: bool


class RequestFailedGoogleRequest(Exception):
    pass


def google_request(params: UserInput, maximum_retries: int = 25) -> GoogleRequestResponse:
    """Execute a Google request with retries"""
    response_data = None
    successfully_scraped = False
    response_headers = None
    google_config = get_google_night_price_config(params)
    request_params: RequestParameters = {
        "url": google_config["url"],
        "request_proxy": params["request_proxy"],
        "request_headers": google_config["headers"],
        "request_cookies": google_config["cookies"],
        "request_type": google_config["type"],
    }

    # Only add request_proxy if it's not None
    if params["request_proxy"] is not None:
        request_params["request_proxy"] = params["request_proxy"]

    print(f"Request params: {request_params}")

    for i in range(maximum_retries):
        try:
            response = Request(params=request_params).curl_request_api_get()
            print(f"Response status code: {response['response'].status_code}")

            if response["response"].status_code == 200:
                response_data = response["response"].text
                response_headers = response["response"].headers
                print(f"Response headers: {response_headers}")
                successfully_scraped = True
                print("successfully scraped")
                break
            else:
                raise RequestFailedGoogleRequest(f"Request failed with status code {response['response'].status_code}")

        except (RequestFailedGoogleRequest, ValueError, ProxyError, Timeout) as e:
            print(f"⚠️  Request retry {i + 1} failed: {e}")
            if i < maximum_retries - 1:  # Don't sleep on last retry
                wait_seconds = 4
                print(f"Waiting {wait_seconds} seconds before next retry")
                time.sleep(wait_seconds)
    
    # If we exhausted all retries and didn't succeed, raise ProxyConnectionEstablishmentError
    if not successfully_scraped:
        from ...exceptions import ProxyConnectionEstablishmentError
        raise ProxyConnectionEstablishmentError(f"All {maximum_retries} retries failed")

    return GoogleRequestResponse(response=response_data or "", successfully_scraped=successfully_scraped, response_headers=response_headers)
