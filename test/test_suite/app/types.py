from typing import TypedDict, NotRequired, Literal, Any
from curl_cffi.requests import Response, ExtraFingerprints


class Run(TypedDict):
    run_id : int
    run_requests_total : int
    run_requests_success : int
    run_requests_failed : int
    run_request_success_rate : float
    run_requests_status_codes : dict[int, str]
    run_time_total : str
    run_time_request_average : str
    
class ProviderParameters(TypedDict):
    provider_headers : dict[str, str]
    provider_cookies : NotRequired[dict[str, str]]
    provider_body : NotRequired[dict[str, Any] | str]

class RequestResponseDebugDetails(TypedDict):
    request_fingerprint : NotRequired[dict[str, Any]]
    request_headers : NotRequired[dict[str, str]]
    response : Any
    request_retries : int
    request_successful : bool
    request_time : str
    request_status_code : int

class RunRequest(RequestResponseDebugDetails):
    request_url : str
    request_id : int
    request_time : str
    request_proxy : str

class ProxyParameters(TypedDict):
    proxy_provider : str
    proxy_host : str
    proxy_port : int
    proxy_username : str
    proxy_password : str
    proxy_iso : str
    proxy_expected_outcome : NotRequired[Any]
    

    
class UserInput(TypedDict):
    provider_id : str
    request_check_in_date : str
    request_nights : int
    request_currency : NotRequired[Literal["USD", "EUR", "GBP"]]
    request_adults : int
    request_proxy : str | None
    request_request_type : Literal["GET", "POST"]
    request_provider : Literal["EXPEDIA", "TLSBROWSERLEAK", "HTTPBIN", "HILTON", "GOOGLE", "BOOKING"]
    request_maximum_retries : int
    request_type : Literal["PROXY_TESTING"]
    

class RequestParameters(TypedDict):
    url : str
    request_proxy : NotRequired[str]
    request_headers : NotRequired[dict[str, str]]
    request_cookies : NotRequired[dict[str, str]]
    request_body : NotRequired[str]
    request_type : Literal["GET", "POST"]

class SyncResponse(TypedDict):
    response : Response
    fingerprint : ExtraFingerprints
    request_headers : dict[str, str]
    
    
class TestResults(TypedDict):
    test_passed: bool
    test_proof_url: NotRequired[str]
    test_proof_status_code: NotRequired[int]
    test_expected_outcome: Any
    test_proxy_url: NotRequired[str]
    test_proxy_try : NotRequired[int]
    test_proxy_result : NotRequired[str]
