import json

from ..types import ProxyParameters

def get_all_proxies_from_file(file_path : str) -> list[ProxyParameters]:
    with open(file_path) as f:
        return json.load(f)