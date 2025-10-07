import json
from textwrap import indent
from typing import Any, TypedDict

from ..types_google import Provider
from .single_provider_details_parser import ParseSingleProviderDetails


class SinglePlaceParserResponse(TypedDict):
    sold_out: bool
    providers: list[Provider]
    successfully_parsed: bool
    country_code: str


class SinglePlaceParserError(Exception):
    pass


class SinglePlaceParser:
    def __init__(self, response: Any):
        self.response: list[Any] = response if isinstance(response, list) else []

    def get_providers(self) -> list[Any] | None:
        try:
            data = self.response
            if len(data) <= 6:
                print("Index [6] doesn't exist in response")
                return None

            # Check if index 35 exists in data[6]
            if len(data[6]) <= 35:
                print("Index [6][35] doesn't exist in response")
                return None

            # Check if index 44 exists in data[6][35]
            if not isinstance(data[6][35], list) or len(data[6][35]) <= 44:
                print("Index [6][35][44] doesn't exist in response")
                return None

            # Now safely access the provider block
            provider_block = data[6][35][44]

            if provider_block:
                return provider_block
            else:
                print("Provider block exists but is empty")
                return None

        except SinglePlaceParserError as e:
            print(f"Error while getting providers: {e!s}")
            return None

    def _get_country_code(self) -> str | None:
        country_code = self.response[6][113]
        if country_code:
            return country_code
        else:
            return None

    def get_place_details(self) -> SinglePlaceParserResponse:
        provider_details_list: list[Provider] = []
        successfully_parsed = False
        providers = self.get_providers()
        country_code = self._get_country_code()
        with open("test/test_suite/app/providers/google/debug/parsed_providers.json", "w") as f:
            json.dump(providers, f,  indent=4)
        if providers:
            for provider in providers:
                provider_details = ParseSingleProviderDetails(provider).get_provider_details()
                if provider_details["successfully_parsed"] and provider_details["provider"] and country_code is not None:
                    provider_details_list.append(provider_details["provider"])
            successfully_parsed = True

            return SinglePlaceParserResponse(
                sold_out=False, providers=provider_details_list, successfully_parsed=successfully_parsed, country_code=country_code
            )

        else:
            return SinglePlaceParserResponse(sold_out=True, providers=[], successfully_parsed=successfully_parsed, country_code=country_code)
