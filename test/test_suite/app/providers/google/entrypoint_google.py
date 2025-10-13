import datetime
import json
from typing import Any
from .request_google import google_request
from ...types import UserInput
from .service.check_proxy_currency_google_service import check_proxy_currency_google_service

def entrypoint_google(params : UserInput) -> Any:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if params["request_type"] == "PROXY_TESTING":
        test_results = check_proxy_currency_google_service(params)
        with open(f"test/test_suite/app/providers/google/debug/proxy_testing_{timestamp}.json", "w") as f:
            json.dump(test_results, f, indent=4)
        
    return google_request(params)


if __name__ == "__main__":
    entrypoint_google(UserInput(
        provider_id="0x89c6c96eba3e2c85:0xc420d3f9c9e9c59e",
        # provider_id="0x14a1bbada8ec898f:0xf42dbcec3657f977",
        request_check_in_date="2026-01-01",
        request_nights=1,
        request_adults=2,
        request_proxy="will be filled by the service",
        request_request_type="GET",
        request_provider="GOOGLE",
        request_maximum_retries=1,
        request_type="PROXY_TESTING",
    ))