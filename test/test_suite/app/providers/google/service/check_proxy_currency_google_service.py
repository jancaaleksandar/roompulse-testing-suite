import json
from ....types import UserInput
from ..common.clean_response_common import CleanResponse
from ..parsers.place_parser import SinglePlaceParser
from ..request_google import google_request
from ....utils.get_all_proxies import get_all_proxies_from_file
from ....exceptions import MissingProxyURL, CheckProxyCurrencyServiceError
from ....types import TestResults



def check_proxy_currency_google_service(params: UserInput) -> list[TestResults]:
    if params["request_proxy"] is None:
        raise MissingProxyURL("Proxy URL is required")
    all_proxies = get_all_proxies_from_file("test/test_suite/app/providers/google/data/scrapoxy_proxies_for_test.json")
    print(f"All proxies: {all_proxies}")
    test_results: list[TestResults] = []

    for proxy in all_proxies:
        print("-" * 50)
        print(f"Proxy: {proxy}")
        print("-" * 50)
        proxy_url = (f"http://{proxy['proxy_username']}:{proxy['proxy_password']}@{proxy['proxy_host']}:{proxy['proxy_port']}")

        print(f"\n{'=' * 50}")
        print(f"Proxy: {proxy_url}")
        print(f"{'=' * 50}\n")

        try:
            expected_outcome = proxy.get("proxy_expected_outcome") if proxy.get("proxy_expected_outcome") else proxy["proxy_iso"]
            params["request_proxy"] = proxy_url
            print(f"\nTrying proxy: {proxy_url}")

            response = google_request(params)
            response_headers = response["response_headers"]

            x_frame_options = response_headers.get("x-frame-options", "NOT_FOUND")
            print(f"X-Frame-Options: {x_frame_options}")

            with open("test/test_suite/app/providers/google/debug/response.html", "w") as f:
                json.dump(response["response"], f, indent=4)

            if not response["successfully_scraped"]:
                print(f"Failed with proxy {proxy_url}")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_result=f"Failed to scrape response - X-Frame-Options: {x_frame_options}",
                    )
                )
                continue

            cleaned_response = CleanResponse(response=response["response"]).clean_response()
            if not cleaned_response["success"] or cleaned_response["data"] is None:
                print(f"Failed to clean response with proxy {proxy_url}")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_result=f"Failed to clean response - X-Frame-Options: {x_frame_options}",
                    )
                )
                continue

            with open("test/test_suite/app/providers/google/debug/cleaned_response.json", "w") as f:
                json.dump(cleaned_response, f, indent=4)

            single_place_parser_response = SinglePlaceParser(response=cleaned_response["data"]).get_place_details()
            if not single_place_parser_response["successfully_parsed"]:
                print(f"Failed to parse providers with proxy {proxy_url}")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_result=f"Failed to parse response - X-Frame-Options: {x_frame_options}",
                    )
                )
                continue

            with open("test/test_suite/app/providers/google/debug/parsed_single_place_parser_response.json", "w") as f:
                json.dump(single_place_parser_response, f, indent=4)

            # Check if country_code is None - if so, mark proxy as wrong
            country_code = single_place_parser_response.get("country_code")
            response_currency = single_place_parser_response.get("response_currency")
            if response_currency is None:
                print(f"Response currency is None with proxy {proxy_url}")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_result=f"Response currency not found - X-Frame-Options: {x_frame_options}",
                    )
                )
                continue

            # Remove the early exit for None country_code - we'll check currency instead
            # if country_code is None and response_currency is not None:
            #     print(f"Country code is None with proxy {proxy_url} - marking as WRONG PROXY")
            #     test_results.append(
            #         TestResults(
            #             test_passed=False,
            #             test_expected_outcome=expected_outcome,
            #             test_proxy_url=f"{proxy_url} (WRONG - country_code is None)",
            #             test_proxy_result=f"Country code not found (currency: {response_currency}) - X-Frame-Options: {x_frame_options}",
            #         )
            #     )
            #     continue

            if not single_place_parser_response["providers"] or len(single_place_parser_response["providers"]) == 0:
                print(f"No providers found with proxy {proxy_url} response : {single_place_parser_response}")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                        test_proxy_result=f"No providers found (country_code: {country_code}) - X-Frame-Options: {x_frame_options}",
                    )
                )
                continue

            with open("test/test_suite/app/providers/google/debug/parsed_providers.json", "w") as f:
                json.dump(single_place_parser_response, f, indent=4)

            # Check if expected outcome matches either country code OR currency
            match_found = False
            for provider in single_place_parser_response["providers"]:
                provider_url = provider.get("provider_offer_url", None)
                if not provider_url:
                    print("No provider URL found")
                    continue
                print(f"Provider URL: {provider_url}")
                print(f"Expected outcome: {expected_outcome}")
                print(f"Country code from response: {country_code}")
                print(f"Response currency: {response_currency}")

                # Match if expected outcome equals country code OR currency
                if str(expected_outcome) == str(country_code) or str(expected_outcome) == str(response_currency):
                    print(f"Found matching provider with proxy {proxy_url}")
                    test_results.append(
                        TestResults(
                            test_passed=True,
                            test_proof_url=provider_url,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=proxy_url,
                            test_proxy_result=f"{country_code} - {response_currency} - X-Frame-Options: {x_frame_options}",
                        )
                    )
                    print(f"Successfully found matching provider with proxy {proxy_url}")
                    match_found = True
                    break
            
            if not match_found:
                # No match found - but provide different message if country_code is None
                if country_code is None:
                    print(f"Country code is None with proxy {proxy_url}, currency: {response_currency}, expected: {expected_outcome}")
                    test_results.append(
                        TestResults(
                            test_passed=False,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=f"{proxy_url} (country_code is None)",
                            test_proxy_result=f"Country code not found, currency mismatch (got currency: {response_currency}, expected: {expected_outcome}) - X-Frame-Options: {x_frame_options}",
                        )
                    )
                else:
                    print(f"No match found for expected outcome '{expected_outcome}' (got: {country_code}/{response_currency})")
                    test_results.append(
                        TestResults(
                            test_passed=False,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=proxy_url,
                            test_proxy_result=f"Mismatch (got: {country_code} - {response_currency}, expected: {expected_outcome}) - X-Frame-Options: {x_frame_options}",
                        )
                    )

        except MissingProxyURL:
            print(f"Proxy URL is required")
            test_results.append(
                TestResults(
                    test_passed=False,
                    test_expected_outcome=proxy.get("proxy_iso", "unknown"),
                    test_proxy_url=proxy_url,
                    test_proxy_result="Error: Proxy URL is required",
                )
            )
            continue

        except CheckProxyCurrencyServiceError as e:
            print(f"Error with proxy {proxy_url}: {e!s}")
            test_results.append(
                TestResults(
                    test_passed=False,
                    test_expected_outcome=proxy.get("proxy_iso", "unknown"),
                    test_proxy_url=proxy_url,
                    test_proxy_result=f"Error: {e!s}",
                )
            )
            continue
                
    return test_results
