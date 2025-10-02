import csv
import json
from typing import TypedDict


class ProxyObject(TypedDict):
    proxy_provider: str
    proxy_host: str
    proxy_port: int
    proxy_username: str
    proxy_password: str
    proxy_iso: str
    proxy_url: str


def csv_to_proxies():
    # # First read existing proxies
    with open("test/scrapoxy/data/all_proxies.json") as f:
        all_proxies: list[ProxyObject] = json.load(f)

    # Now process the CSV
    with open("test/scrapoxy/debug/all_proxies_ip_royal.csv") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            ip_port_user_pass, iso = row

            # Handle both formats
            if "@" in ip_port_user_pass:
                # Format: USERNAME:PASSWORD@IP:PORT
                user_pass, ip_port = ip_port_user_pass.split("@")
                username, password = user_pass.split(":")
                ip, port = ip_port.split(":")
            else:
                # Format: IP:PORT:USERNAME:PASSWORD
                parts = ip_port_user_pass.split(":")
                ip, port, username, password = parts

            proxy_object: ProxyObject = {
                "proxy_provider": "iproyal",
                "proxy_host": ip,
                "proxy_port": int(port),
                "proxy_username": username,
                "proxy_password": password,
                "proxy_iso": iso,
                "proxy_url": f"http://{username}:{password}@{ip}:{port}",
            }
            all_proxies.append(proxy_object)

    # # Write back the combined results
    with open("test/scrapoxy/data/all_proxies.json", "w") as f:
        json.dump(all_proxies, f, indent=4)
    # print(all_proxies)


if __name__ == "__main__":
    csv_to_proxies()
