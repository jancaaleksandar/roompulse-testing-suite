import re
from typing import Any, TypedDict
import urllib.parse

from ..types_google import Provider


class PriceParserException(Exception):
    pass


class ParsingSingleProviderDetailsResponse(TypedDict):
    provider: Provider | None
    successfully_parsed: bool


class ParseSingleProviderDetails:
    def __init__(self, response: list[Any]):
        self.response = response

    def get_provider_name(self):
        return self.response[0]

    def get_provider_url(self):
        full_url = self.response[5][0]

        # Extract the actual destination URL after &pcurl=
        if "&pcurl=" in full_url:
            # Split the URL and get the part after &pcurl=
            destination_url = full_url.split("&pcurl=")[1]
            # Decode the URL
            decoded_url = urllib.parse.unquote(destination_url)
            # Limit to 900 characters to fit in database
            return decoded_url[:900]
        else:
            print("No &pcurl= found in URL")
            # Decode the URL
            decoded_url = urllib.parse.unquote(full_url)
            return decoded_url[:900]

    def get_provider_price(self) -> dict[str, float | str]:
        raw_price = self.response[1]
        print(f"raw_price: {raw_price}")

        # If raw_price is already a dictionary with amount and currency
        if isinstance(raw_price, dict) and "amount" in raw_price and "currency" in raw_price:
            raw_dict = dict(raw_price)  # type: ignore
            amount = float(raw_dict.get("amount", 0))  # type: ignore
            currency = str(raw_dict.get("currency", None))  # type: ignore
            return {"amount": amount, "currency": currency}

        # If it's a string like '65\xa0€'
        if isinstance(raw_price, str):
            # Remove thousand separators like commas e.g., '1,000' -> '1000'
            sanitized_price = raw_price.replace(",", "")
            amount_match = re.search(r"(\d+(?:\.\d+)?)", sanitized_price)
            amount = float(amount_match.group(1)) if amount_match else 0

            # Identify currency
            currency_map = {
                "€": "EUR",
                "$": "USD",
                "£": "GBP",
                "¥": "JPY",
                "₹": "INR",
                "CHF": "CHF",
                "A$": "AUD",
                "C$": "CAD",
                "₺": "TRY"

                # Add more currency mappings as needed
            }

            currency = "USD"  # Default
            for symbol, code in currency_map.items():
                if symbol in raw_price:
                    currency = code
                    break

            return {"amount": amount, "currency": currency}

        # Fallback
        return {
            "amount": 0,  # TODO: remove this SET TO NONE
            "currency": "USD",
        }

    def get_is_provider_brand_offer(self):
        brand_offer_block = self.response[11]
        if brand_offer_block:
            # # Convert to string for consistent checking, regardless of data type
            # brand_offer_str = str(brand_offer_block).lower()

            # if "site" in brand_offer_str:
            return True
        return False

    def get_provider_icon_url(self):
        icon_url_string = self.response[8]
        if icon_url_string:
            # logic to remove the "//" from the start of the string
            if icon_url_string.startswith("//"):
                return icon_url_string[2:]
            return icon_url_string
        return None

    def get_provider_details(self) -> ParsingSingleProviderDetailsResponse:
        successfully_parsed = False
        try:
            # Get the provider name with fallback to None if it fails
            try:
                provider_name = self.get_provider_name()
            except (IndexError, TypeError, KeyError):
                provider_name = None

            # Get provider icon URL with fallback to None if it fails
            try:
                provider_icon_url = self.get_provider_icon_url()
            except (IndexError, TypeError, KeyError):
                provider_icon_url = None

            # Get provider URL with fallback to None if it fails
            try:
                provider_url = self.get_provider_url()
            except (IndexError, TypeError, KeyError):
                provider_url = None

            # Get price details with fallbacks if it fails
            try:
                price_details = self.get_provider_price()
                price_amount = price_details.get("amount")
                price_currency = price_details.get("currency")
            except (IndexError, TypeError, KeyError, AttributeError):
                price_amount = None
                price_currency = None

            # Get brand offer status with fallback to False if it fails
            try:
                is_brand_offer = self.get_is_provider_brand_offer()
            except (IndexError, TypeError, KeyError):
                is_brand_offer = False

            successfully_parsed = True

            return ParsingSingleProviderDetailsResponse(
                provider=Provider(
                    provider_name=str(provider_name or None),
                    provider_icon_url=str(provider_icon_url or None),
                    provider_offer_url=str(provider_url or None),
                    provider_offer_is_brand_offer=is_brand_offer,
                    provider_offer_price_amount=float(price_amount if price_amount is not None else 0),
                    provider_offer_price_currency=str(price_currency or None),
                    provider_offer_is_sold_out=False,
                ),
                successfully_parsed=successfully_parsed,
            )
        except PriceParserException:
            return ParsingSingleProviderDetailsResponse(provider=None, successfully_parsed=False)
