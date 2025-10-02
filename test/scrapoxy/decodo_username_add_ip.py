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


def decodo_username_add_ip():
    print("Starting to process proxies...")

    with open("test/scrapoxy/data/all_proxies.json") as f:
        all_proxies: list[ProxyObject] = json.load(f)

    print(f"Loaded {len(all_proxies)} proxies")
    decodo_count = 0

    for proxy in all_proxies:
        if proxy["proxy_provider"] == "decodo":
            old_username = proxy["proxy_username"]
            original_ip = proxy["proxy_host"]

            # Create username in format: user-spfrgk8g21-ip-166.0.77.151
            new_username = f"user-{old_username}-ip-{original_ip}"

            # Update to use isp.decodo.com as host (per Decodo docs)
            proxy["proxy_host"] = "isp.decodo.com"
            proxy["proxy_port"] = 10001
            proxy["proxy_username"] = new_username
            proxy["proxy_url"] = f"http://{new_username}:{proxy['proxy_password']}@isp.decodo.com:10001"

            decodo_count += 1
            print(f"Updated: {new_username}")

    print(f"\nUpdated {decodo_count} decodo proxies")

    with open("test/scrapoxy/data/all_proxies.json", "w") as f:
        json.dump(all_proxies, f, indent=4)


if __name__ == "__main__":
    decodo_username_add_ip()
