from typing import Any, TypedDict, Optional
from hotel_info_lib import Request, RequestParameters
from ...types import UserInput
from .booking_config import get_booking_config
from curl_cffi import Response
from curl_cffi.requests.exceptions import ProxyError, Timeout
import time

class BookingRequestError(Exception):
    pass

class ScrapedData(TypedDict):
    url: str
    actual_response: Response

class BookingRequestResponse(TypedDict):
    successfully_scraped: bool
    scraped_data: ScrapedData


def booking_request(params: UserInput, maximum_retries: int = 30) -> BookingRequestResponse:
    successfully_scraped = False
    sync_resp: Any = None
    url = None
    err_msg: Optional[str] = None
    last_status_code: Optional[int] = None

    config = get_booking_config(params)
    # Keep URL early so we can report it on failures too
    url = config["url"]

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
        request_proxy=params["request_proxy"],
    )

    print(f"Request params: {request_params}")

    for i in range(maximum_retries):
        try:
            request = Request(params=request_params)
            sync_resp = request.curl_request_api_get() if request_params["request_type"] == "GET" else request.curl_request_api_post()

            if not sync_resp:
                raise BookingRequestError("Request returned no response")

            actual = None
            if hasattr(sync_resp, 'response'):
                actual = sync_resp.response
            elif isinstance(sync_resp, dict) and 'response' in sync_resp:
                actual = sync_resp['response']  # type: ignore[index]

            if actual is None:
                raise BookingRequestError("No underlying response object present")

            status_code = getattr(actual, 'status_code', None)
            last_status_code = status_code
            print(f"Response status code: {status_code}")

            # Treat proxy-related statuses as retryable errors
            if status_code in (403, 407):
                raise BookingRequestError(f"Proxy failed/auth required (status {status_code})")

            # For any other status, return the response (mark success only for 200)
            successfully_scraped = (status_code == 200)
            break

        except (BookingRequestError, ValueError, ProxyError, Timeout) as e:
            err_msg = f"{type(e).__name__}: {e!s}"
            print(f"⚠️  Request retry {i + 1} failed: {e}")
            if i < maximum_retries - 1:  # Don't sleep on last retry
                print(f"retry count {i}")

    actual_response: Optional[Response] = None
    if sync_resp:
        if hasattr(sync_resp, 'response'):
            actual_response = sync_resp.response
        elif isinstance(sync_resp, dict) and 'response' in sync_resp:
            actual_response = sync_resp['response']  # type: ignore[index]

    # If we got a non-proxy response, return it even if not 200
    # Only raise if we never got a response or if the last status indicates proxy failure
    if not url or actual_response is None or (last_status_code in (403, 407)):
        # Build a detailed error message including any available response info
        parts: list[str] = []
        if url:
            parts.append(f"url={url}")
        if err_msg:
            parts.append(f"root_error={err_msg}")
        if actual_response is not None:
            try:
                status = getattr(actual_response, 'status_code', None)
                if status is not None:
                    parts.append(f"status_code={status}")
                text_preview = getattr(actual_response, 'text', '')
                if isinstance(text_preview, str) and text_preview:
                    snippet = text_preview[:400].replace('\n', ' ').replace('\r', ' ')
                    parts.append(f"body_snippet={snippet}")
            except Exception:
                # best effort; ignore issues while building debug info
                pass
        detail = "; ".join(parts) if parts else "(no further details)"
        raise BookingRequestError(f"Failed to scrape data: {detail}")

    return BookingRequestResponse(
        successfully_scraped=successfully_scraped,
        scraped_data=ScrapedData(url=url, actual_response=actual_response),
    )
