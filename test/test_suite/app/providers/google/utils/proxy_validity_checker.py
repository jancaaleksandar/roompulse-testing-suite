from typing import Any, Callable


class ProxyValidityChecker:
    def __init__(self, location: str, expected_result: str, response: Any):
        self.location = location.upper()
        self.expected_result = expected_result
        self.response = response
        
        # Define the mapping inside __init__ so methods are available
        self.location_matching: dict[str, Callable[[], bool]] = {
            "UNITED_STATES": self.check_currency, # scrapoxy
            "UNITED_KINGDOM": self.check_currency, # scrapoxy
            "ISRAEL": self.check_country_iso, # geonode
            "CANADA": self.check_currency_in_provider_url, # geonode
            "GREECE" : self.check_country_iso, # geonode
            "AUSTRALIA": self.check_currency_in_provider_url, # scrapoxy
            "SWITZERLAND": self.check_currency, # geonode
            "TURKEY" : self.check_country_iso, # geonode
            "SINGAPORE": self.check_currency_in_provider_url, # scrapoxy
            "GERMANY": self.check_country_iso, # scrapoxy
        }

    def check_country_iso(self) -> bool:
        """Check if expected result matches the country ISO in response."""
        country_iso = self.response.get('country_code')
        if country_iso and self.expected_result == country_iso:
            return True
        return False

    def check_currency_in_provider_url(self) -> bool:
        """Check if country ISO appears in any provider URL."""
        providers = self.response.get("providers", [])
        if not providers:
            return False
            
        for provider in providers:
            provider_url = provider.get('provider_offer_url', '')
            if provider_url and self.expected_result.lower() in provider_url.lower():
                print(f"✅ Proxy validation PASSED with proxy {provider_url}")
                return True
        return False

    def check_currency(self) -> bool:
        """Check if expected result matches the currency in response."""
        currency = self.response.get('response_currency')
        if currency and self.expected_result == currency:
            return True
        return False

    def validate(self) -> bool:
        """
        Main method to run the appropriate validation based on location.
        Returns True if validation passes, False otherwise.
        """
        check_method = self.location_matching.get(self.location)
        
        if check_method is None:
            print(f"Warning: No validation method defined for location '{self.location}'")
            # Default to checking country ISO
            return self.check_country_iso()
        
        return check_method()