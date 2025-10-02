import json
import time

from curl_cffi.requests.errors import RequestsError
from requests.exceptions import RequestException

from ...types import RequestParameters, RequestResponseDebugDetails, RunRequest

# from .request_versions.request_final import Request
from ...utils.http.request_http import Request


class RequesFailedExpediaRequest(Exception):
    pass


def expedia_request(params: RequestParameters, request_id: int) -> list[RunRequest]:
    """Execute a single request with retries - designed to be run in a thread"""
    url = params["url"]
    request_proxy_str = params.get("request_proxy", None)
    if request_proxy_str is None:
        raise RequesFailedExpediaRequest("No proxies found")
    request_maximum_retries = 15

    all_request_responses_debug_details: list[RequestResponseDebugDetails] = []
    iteration_start_time = time.time()  # Initialize outside loop

    # Initialize persistent cookie storage
    persistent_cookies = {}

    for i in range(request_maximum_retries):
        print("-" * 50)
        response = None  # Initialize response to avoid unbound variable error
        try:
            iteration_start_time = time.time()

            # Add persistent cookies to the request parameters
            if persistent_cookies:
                # Update request_cookies in params
                # request_cookies = params.get("request_cookies") or {}
                # request_cookies.update(persistent_cookies)  # type: ignore
                # params["request_cookies"] = request_cookies  # type: ignore

                # Also add to headers as Cookie header
                cookie_header = "; ".join(f"{name}={value}" for name, value in persistent_cookies.items())  # type: ignore
                request_headers = params.get("request_headers") or {}
                request_headers["Cookie"] = cookie_header  # type: ignore
                params["request_headers"] = request_headers  # type: ignore
                # random_int = random.randint(1, 1000000)
                # with open(f"request_headers_{random_int}.json", "w") as f:
                #     json.dump(request_headers, f, indent=4)

                # print(f"🍪 Using persistent cookies in request {i+1}: {persistent_cookies}")

            # Use the params from the outer loop directly
            response = Request(params=params).curl_request_api_post()
            print(response["response"].status_code)
            try:
                response_data = response["response"].json()  # type: ignore
            except json.JSONDecodeError:
                response_data = {"text": response["response"].text}

            # Extract cookies from successful response
            if hasattr(response["response"], "cookies") and response["response"].cookies:
                try:
                    cookie_jar = response["response"].cookies
                    cookies_dict = {name: value for name, value in cookie_jar.items()}
                    print(f"✅ Success cookies found: {len(cookies_dict)} cookies")

                    # Extract bm_s cookie for persistent use
                    if "bm_s" in cookies_dict:
                        persistent_cookies["bm_s"] = cookies_dict["bm_s"]
                        print(f"🎯 Captured bm_s from successful response (status {response['response'].status_code})")
                except (AttributeError, KeyError, ValueError) as cookie_error:
                    print(f"Error extracting cookies from successful response: {cookie_error}")

            iteration_end_time = time.time()
            iteration_time = str(iteration_end_time - iteration_start_time)

            # Determine if this attempt was successful
            is_successful = response["response"].status_code == 200
            if not is_successful:
                raise RequesFailedExpediaRequest(
                    f"Request {request_id} failed with status code {response['response'].status_code}"
                )

            request_response_debug_details = RequestResponseDebugDetails(
                request_fingerprint=response["fingerprint"].__dict__,
                request_headers=response["request_headers"],
                response=response_data,
                request_retries=i,
                request_successful=is_successful,
                request_time=iteration_time,
                request_status_code=response["response"].status_code,
            )

            all_request_responses_debug_details.append(request_response_debug_details)

            if is_successful:
                break
            # If not successful, continue to next retry (the loop will handle this)

        except (RequestException, RequestsError, ConnectionError, TimeoutError) as e:
            print(f"⚠️  Request {request_id} retry {i + 1} failed: {e}")
            iteration_end_time = time.time()
            iteration_time = str(iteration_end_time - iteration_start_time)
            wait_random_seconds = 3

            # Create RequestResponseDebugDetails for failed response if we have response data
            if "response" in locals() and response and "response" in response:
                try:
                    # Try to get response data
                    try:
                        response_data = response["response"].json()  # type: ignore
                    except json.JSONDecodeError:
                        response_data = {"text": response["response"].text, "error": str(e)}

                    # Create debug details for failed response
                    fingerprint_dict = {}
                    fingerprint_dict = response["fingerprint"].__dict__ if response.get("fingerprint") else {}

                    request_response_debug_details = RequestResponseDebugDetails(
                        request_fingerprint=fingerprint_dict,
                        request_headers=response.get("request_headers", {}),
                        response=response_data,
                        request_retries=i,
                        request_successful=False,
                        request_time=iteration_time,
                        request_status_code=response["response"].status_code
                        if hasattr(response["response"], "status_code")
                        else 999,
                    )

                    all_request_responses_debug_details.append(request_response_debug_details)

                    # Extract cookies if response exists
                    cookie_jar = response["response"].cookies
                    cookies_dict = {}
                    if hasattr(cookie_jar, "items"):
                        for name, value in cookie_jar.items():
                            cookies_dict[name] = value

                        if "bm_s" in cookies_dict:
                            persistent_cookies["bm_s"] = cookies_dict["bm_s"]
                            print(f"🎯 Captured bm_s from failed response (status {response['response'].status_code})")

                except (AttributeError, KeyError, TypeError) as response_error:
                    print(f"Error processing failed response: {response_error}")
                    # Create minimal debug details for completely failed request
                    request_response_debug_details = RequestResponseDebugDetails(
                        request_fingerprint={},
                        request_headers={},
                        response={"error": str(e), "processing_error": str(response_error)},
                        request_retries=i,
                        request_successful=False,
                        request_time=iteration_time,
                        request_status_code=999,
                    )
                    all_request_responses_debug_details.append(request_response_debug_details)
            else:
                print("No response available to extract cookies from")

            print(f"Waiting {wait_random_seconds} seconds before next retry")
            time.sleep(wait_random_seconds)
            continue

    # Note: else block removed since we now capture all responses (successful and failed) within the loop

    # Convert to RunRequest objects
    run_requests: list[RunRequest] = []
    for request_response_debug_detail in all_request_responses_debug_details:
        # Use the actual time for this specific iteration
        specific_iteration_time = request_response_debug_detail["request_time"]

        run_request = RunRequest(
            request_fingerprint=request_response_debug_detail.get("request_fingerprint", {}),
            request_headers=request_response_debug_detail.get("request_headers", {}),
            request_id=request_id,
            request_proxy=request_proxy_str,
            request_retries=request_response_debug_detail["request_retries"],
            request_successful=request_response_debug_detail["request_successful"],
            request_time=specific_iteration_time,
            request_url=url,
            response=request_response_debug_detail["response"],
            request_status_code=request_response_debug_detail["request_status_code"],
        )
        run_requests.append(run_request)

    return run_requests
