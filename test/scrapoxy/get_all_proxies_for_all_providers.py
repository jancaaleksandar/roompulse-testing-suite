URL_PATH_FOR_GET_ALL_PROXIES_FOR_PROVIDERS = "/api/scraper/project/connectors"
SCRAPOXY_HOST = "scrapoxy.roompulse.internal"
SCRAPOXY_SWAGGER_PORT = 8890
# MTO
PROJECT_USERNAME = "w4l5227ces9ijsa6w8uipm"
PROJECT_PASSWORD = "a3ojfg0nwwxq8obozlg1"
# IRELAND
# PROJECT_USERNAME = "u5cfakq7sclif2qixsdp"
# PROJECT_PASSWORD = "xf0rtgbsb88ny48mmnh3h"
# expedia uk-us
# PROJECT_USERNAME = "9svgtitg6p8sb81gknfpzd"
# PROJECT_PASSWORD = "vbtc0tz0xjre9sq4f5kjqo"
# unitedkingdom gneeral iproyal
# PROJECT_USERNAME = "d1ypajmd93b03tjylw2bp1l"
# PROJECT_PASSWORD = "lgkqulwr2adhy440w1s8ub"
# unitedstates general iproyal
# PROJECT_USERNAME = "vrgrub8jsp1poht3qch8"
# PROJECT_PASSWORD = "7gq4vun974sy43wgasq7z"
# PROJECT_ID = "43cf4fa4-8644-48fc-85e7-285512004e7e"
DECODO_USERNAME = "spfrgk8g21"
DECODO_PASSWORD = "j_Rc8gppu58EZzUmb4"


import base64
import json
from typing import NotRequired, TypedDict

import requests


class ProxyObject(TypedDict):
    proxy_provider: str
    proxy_host: str
    proxy_port: int | None
    proxy_username: str
    proxy_iso: str
    proxy_password: str
    proxy_url: NotRequired[str]


def get_all_proxies_for_all_providers():
    url = f"http://{SCRAPOXY_HOST}:{SCRAPOXY_SWAGGER_PORT}{URL_PATH_FOR_GET_ALL_PROXIES_FOR_PROVIDERS}"
    auth = base64.b64encode(f"{PROJECT_USERNAME}:{PROJECT_PASSWORD}".encode()).decode()
    all_proxies: list[ProxyObject] = []

    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(url, headers=headers, timeout=10)
    all_connectors_data = response.json()
    with open("test/scrapoxy/debug/all_proxies_for_all_providers.json", "w") as f:
        json.dump(all_connectors_data, f, indent=4)
    for connector in all_connectors_data:
        proxies = connector["proxies"]
        for proxy in proxies:
            if proxy["type"] == "iproyal-server":
                continue
            proxy_object: ProxyObject = {
                "proxy_provider" : proxy["type"],
                "proxy_host": proxy["fingerprint"]["ip"],
                "proxy_port": int(proxy["name"].split(":")[1]) if ":" in proxy["name"] else int(proxy["name"]),
                "proxy_username": PROJECT_USERNAME,
                "proxy_password": PROJECT_PASSWORD,
                "proxy_iso" : proxy["fingerprint"]["countryCode"],
                "proxy_url": f"http://{PROJECT_USERNAME}:{PROJECT_PASSWORD}@{proxy['fingerprint']['ip']}:{proxy['name'].split(':')[1] if ':' in proxy['name'] else proxy['name']}",
            }
            if proxy_object["proxy_provider"] == "decodo":
                proxy_object["proxy_username"] = DECODO_USERNAME
                proxy_object["proxy_password"] = DECODO_PASSWORD
                
            all_proxies.append(proxy_object)
    with open("test/scrapoxy/data/all_proxies.json", "w") as f:
        json.dump(all_proxies, f, indent=4)


if __name__ == "__main__":
    get_all_proxies_for_all_providers()
