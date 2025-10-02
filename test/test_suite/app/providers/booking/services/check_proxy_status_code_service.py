# from ....utils.get_all_proxies import get_all_proxies_from_file
# from ....types import UserInput, TestResults
# from ....exceptions import MissingProxyURL
# def check_proxy_status_code_service(params: UserInput) -> list[TestResults]:
#     if params["request_proxy"] is None:
#         raise MissingProxyURL("Proxy URL is required")
#     all_proxies = get_all_proxies_from_file("test/test_suite/app/providers/booking/data/proxy_testing.json")
#     for proxy in all_proxies:
#         proxy_url = (f"http://{proxy['proxy_username']}:{proxy['proxy_password']}@{proxy['proxy_host']}:{proxy['proxy_port']}")
#         try:
#             expected_outcome = 200
#             params["request_proxy"] = proxy_url
#             print(f"\nTrying proxy: {proxy_url}")

#             response = booking_request(params)
#             with open("test/test_suite/app/providers/booking/debug/response.json", "w") as f:
#                 json.dump(response, f, indent=4)
    
#     test_results: list[TestResults] = []
    
#     return test_results