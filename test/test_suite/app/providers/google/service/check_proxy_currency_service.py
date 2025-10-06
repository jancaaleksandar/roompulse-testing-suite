import json
from ....types import UserInput
from ..common.clean_response_common import CleanResponse
from ..parsers.place_parser import SinglePlaceParser
from ..request_google import google_request
from ....utils.get_all_proxies import get_all_proxies_from_file
from ....exceptions import MissingProxyURL, CheckProxyCurrencyServiceError
from ....types import TestResults



def check_proxy_currency_service(params: UserInput) -> list[TestResults]:
    if params["request_proxy"] is None:
        raise MissingProxyURL("Proxy URL is required")
    all_proxies = get_all_proxies_from_file("test/test_suite/app/providers/google/data/proxy_testing.json")
    test_results: list[TestResults] = []

    for proxy in all_proxies:
        proxy_url = (
            f"http://{proxy['proxy_username']}:{proxy['proxy_password']}@{proxy['proxy_host']}:{proxy['proxy_port']}"
        )
        try:
            expected_outcome = proxy["proxy_iso"]
            params["request_proxy"] = proxy_url
            print(f"\nTrying proxy: {proxy_url}")

            response = google_request(params)
            with open("test/test_suite/app/providers/google/debug/response.html", "w") as f:
                json.dump(response, f, indent=4)

            if not response["successfully_scraped"]:
                print(f"Failed with proxy {proxy_url}")
                continue

            cleaned_response = CleanResponse(response=response["response"]).clean_response()
            if not cleaned_response["success"] or cleaned_response["data"] is None:
                print(f"Failed to clean response with proxy {proxy_url}")
                continue

            parsed_providers = SinglePlaceParser(response=cleaned_response["data"]).get_place_details()
            if not parsed_providers["successfully_parsed"]:
                print(f"Failed to parse providers with proxy {proxy_url}")
                continue

            if not parsed_providers["providers"] or len(parsed_providers["providers"]) == 0:
                print(f"No providers found with proxy {proxy_url}")
                continue

            with open("test/test_suite/app/providers/google/debug/parsed_providers.json", "w") as f:
                json.dump(parsed_providers, f, indent=4)

            for provider in parsed_providers["providers"]:
                provider_url = provider.get("provider_offer_url", None)
                if not provider_url:
                    print("No provider URL found")
                    continue
                print(f"Provider URL: {provider_url}")
                print(f"Expected outcome: {expected_outcome}")
                if (
                    f"country={expected_outcome}" in provider_url.lower()
                    or f"code={expected_outcome}" in provider_url.lower()
                ):
                    print(f"Found matching provider with proxy {proxy_url}")
                    test_results.append(
                        TestResults(
                            test_passed=True,
                            test_proof_url=provider_url,
                            test_expected_outcome=expected_outcome,
                            test_proxy_url=proxy_url,
                        )
                    )
                    print(f"Successfully found matching provider with proxy {proxy_url}")
                    break
            else:
                # This executes only if the loop completes without breaking (no match found)
                print(f"No match found for expected outcome '{expected_outcome}' in any provider URL")
                test_results.append(
                    TestResults(
                        test_passed=False,
                        test_expected_outcome=expected_outcome,
                        test_proxy_url=proxy_url,
                    )
                )

        except MissingProxyURL:
            print("Proxy URL is required")
            continue

        except CheckProxyCurrencyServiceError as e:
            print(f"Error with proxy {proxy_url}: {e!s}")
            continue
    return test_results
