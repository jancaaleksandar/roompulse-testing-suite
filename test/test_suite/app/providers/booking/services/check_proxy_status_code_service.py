import json
import traceback
from selectors import SelectSelector

from ....exceptions import CheckProxyCurrencyServiceError, MissingProxyURL
from ....types import TestResults, UserInput
from ....utils.get_all_proxies import get_all_proxies_from_file
from ..request_booking import booking_request, BookingRequestResponse, BookingRequestError


def check_proxy_status_code_service(params: UserInput) -> list[TestResults]:
    if params["request_proxy"] is None:
        raise MissingProxyURL("Proxy URL is required")

    all_proxies = get_all_proxies_from_file("test/test_suite/app/data/proxy_testing.json")
    test_results: list[TestResults] = []
    expected_outcome = 200  # We expect a 200 status code

    for proxy in all_proxies:
        for i in range(10):
            proxy_url = (
                f"http://{proxy['proxy_username']}:{proxy['proxy_password']}@{proxy['proxy_host']}:{proxy['proxy_port']}"
            )

            try:
                params["request_proxy"] = proxy_url
                print(f"\nTrying proxy: {proxy_url}")

                booking_request_response : BookingRequestResponse = booking_request(params)

                with open("test/test_suite/app/providers/booking/debug/response.html", "w") as f:
                    f.write(booking_request_response['scraped_data']['actual_response'].text)

                if not booking_request_response["successfully_scraped"]:
                    print(f"Failed with proxy {proxy_url}")
                    test_results.append(
                        TestResults(
                            test_passed=False,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=proxy_url,
                            test_proxy_try=i + 1,
                        )
                    )
                    continue


                status_code = booking_request_response['scraped_data']['actual_response'].status_code
                if status_code == expected_outcome:
                    test_results.append(
                        TestResults(
                            test_passed=True,
                            test_proof_status_code=status_code,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=proxy_url,
                            test_proxy_try=i + 1,
                        )
                    )
                else:
                    test_results.append(
                        TestResults(
                            test_passed=False,
                            test_proof_status_code=status_code,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=proxy_url,
                            test_proxy_try=i + 1,
                        )
                    )
            except MissingProxyURL:
                print("Proxy URL is required")
                continue

            except (BookingRequestError, CheckProxyCurrencyServiceError, ValueError, AttributeError, TypeError, KeyError) as e:
                print(f"Error with proxy {proxy_url}: {e!s}")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_try=i + 1,
                    )
                )
                continue

            except Exception:
                # Unexpected error: print full traceback to help diagnose
                print(f"Unexpected error with proxy {proxy_url}:")
                print(traceback.format_exc())
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_try=i + 1,
                    )
                )
                continue

    return test_results


if __name__ == "__main__":
    # Example usage
    test_params = UserInput(
        provider_id="gr/the-alex",
        request_check_in_date="2025-10-15",
        request_nights=2,
        request_currency="EUR",
        request_adults=2,
        request_proxy="TBA",
        request_request_type="GET",
        request_provider="BOOKING",
        request_maximum_retries=5,
        request_type="PROXY_TESTING",
    )
    results = check_proxy_status_code_service(test_params)
    with open("test/test_suite/app/providers/booking/debug/proxy_testing.json", "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n\nTest Results: {len(results)} proxies tested")
    for result in results:
        print(f"Proxy: {result.get('test_proxy_url', 'N/A')} - Passed: {result['test_passed']}")
