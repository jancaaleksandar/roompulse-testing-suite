import json
from typing import NotRequired, TypedDict


class ProxyObject(TypedDict):
    proxy_provider: str
    proxy_host: str
    proxy_port: int | None
    proxy_username: str
    proxy_iso: str
    proxy_password: str
    proxy_url: NotRequired[str]


def iproyal_change_host():
    print("Starting to process proxies...")

    with open("test/scrapoxy/data/all_proxies.json") as f:
        all_proxies: list[ProxyObject] = json.load(f)

    iproyal_count = 0
    for proxy in all_proxies:
        if proxy["proxy_provider"] == "iproyal":
            # Keep the original IP as the host (e.g., 191.116.125.248)
            # Build proxy URL in format: http://username:password@host:port
            proxy["proxy_url"] = (
                f"http://{proxy['proxy_username']}:{proxy['proxy_password']}@{proxy['proxy_host']}:{proxy['proxy_port']}"
            )
            iproyal_count += 1
            print(f"Updated: {proxy['proxy_url']}")

    print(f"\nUpdated {iproyal_count} iproyal proxies")

    with open("test/scrapoxy/data/all_proxies.json", "w") as f:
        json.dump(all_proxies, f, indent=4)


if __name__ == "__main__":
    iproyal_change_host()
