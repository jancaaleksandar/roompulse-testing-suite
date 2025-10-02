import json

from .providers.expedia.config.expedia_price_config import get_expedia_price_config
from .providers.hilton.config.hilton_price_config import get_hitlon_config
from .providers.httbin.config.httpbin_ip_config import get_httpbin_config
from .types import RequestParameters, UserInput


def parse_cookies(cookies: str | dict[str, str] | None) -> dict[str, str]:
    """Parse cookies from string format to dictionary format"""
    if cookies is None:
        return {}

    if isinstance(cookies, dict):
        return cookies

    # At this point, cookies must be a string
    cookie_dict: dict[str, str] = {}
    # Split by semicolon and parse each cookie
    for cookie in cookies.split(";"):
        cookie = cookie.strip()
        if "=" in cookie:
            key, value = cookie.split("=", 1)  # Split only on first =
            cookie_dict[key.strip()] = value.strip()
    return cookie_dict


class ParameterGenerator:
    def __init__(self, client_input: list[UserInput]):
        self.client_input = client_input

    def generate_request_parameters(self) -> list[RequestParameters]:
        """Convert UserInput list to RequestParameters list"""
        request_parameters_list: list[RequestParameters] = []

        config_generators = {
            "EXPEDIA": get_expedia_price_config,
            "HTTPBIN": get_httpbin_config,
            "HILTON": get_hitlon_config,
        }

        for user_input in self.client_input:
            config = config_generators[user_input["request_provider"]](user_input)

            # Parse cookies properly - handle both string and dict formats
            parsed_cookies = parse_cookies(config.get("cookies"))

            request_params = RequestParameters(
                url=config["url"],
                **({"request_proxy": user_input["request_proxy"]} if user_input["request_proxy"] else {}),
                request_headers=config["headers"],
                request_cookies=parsed_cookies,
                **({"request_body": json.dumps(config["payload"])} if config.get("payload") else {}),
                request_type=user_input["request_request_type"],
            )

            request_parameters_list.append(request_params)

        return request_parameters_list
