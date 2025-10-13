from typing import TypedDict
from browserbase import Browserbase
from browserbase.types.session_create_params import ProxiesUnionMember1, ProxiesUnionMember1ExternalProxyConfig
from playwright.sync_api import sync_playwright, Playwright


class ProxyStructureType(TypedDict):
    host: str
    port: int
    username: str
    password: str

project_id = "1fbc9dd6-8227-4af7-b473-bf9befba128a"
api_key = "bb_live_RA1pJcL7NnwUtcyNwQxuMIyuFUA"

bb = Browserbase(api_key=api_key)

def browserbase_browser_testing(playwright_initiated: Playwright, proxy: ProxyStructureType) -> None:
    print("-" * 50)
    print("STARTING BROWSERBASE TESTING")
    print("-" * 50)

    proxy_config: ProxiesUnionMember1ExternalProxyConfig = {
        "type": "external",
        "server": f"https://{proxy['host']}:{proxy['port']}",
        "username": proxy["username"],
        "password": proxy["password"]
    }
    print(f"DEBUG : got proxy config : {proxy_config}")

    session_bb = bb.sessions.create(
        project_id=project_id,
        proxies=[proxy_config]
    )
    print("DEBUG : got session")

    chromium = playwright_initiated.chromium
    print("DEBUG : got chromium")
    browser = chromium.connect_over_cdp(session_bb.connect_url)
    print("DEBUG : got browser")
    context = browser.contexts[0]
    print("DEBUG : got context")
    page = context.pages[0]
    print("DEBUG : got page")

    try:
        print("DEBUG : trying to go to the page")
        page.goto(
            url="https://www.google.com/maps/place/Best+Western+Plus+Philadelphia-Pennsauken+Hotel/@39.9347213,-75.0755581,16.57z/data=!4m11!3m10!1s0x89c6c96eba3e2c85:0xc420d3f9c9e9c59e!5m4!1s2025-12-21!2i3!4m1!1i2!8m2!3d39.93363!4d-75.07762!16s%2Fg%2F11fcttw9y1?entry=ttu&g_ep=EgoyMDI1MTAwOC4wIKXMDSoASAFQAw%3D%3D",
            wait_until="domcontentloaded",
            timeout=120000)
        print("DEBUG : page loaded")
        page.screenshot(path=f"test/test_suite/app/providers/google/debug/browserbase_browser_screenshot_{proxy["host"]}.png")
    finally:
        page.close()
        browser.close()
        print(f"Session complete! View replay at https://browserbase.com/sessions/{session_bb.id}")

def main() -> None:
    with sync_playwright() as playwright:
        proxy: ProxyStructureType = {
            "host": "isp.decodo.com",
            "port": 10001,
            "username": "user-spfrgk8g21-ip-104.253.147.107",
            "password": "j_Rc8gppu58EZzUmb4"
        }
        # }        proxy: ProxyStructureType = {
        #     "host": "69.176.95.55",
        #     "port": 12323,
        #     "username": "14ab59fe1cc10",
        #     "password": "07c7b5a1e1"
        # }
        browserbase_browser_testing(playwright, proxy)

if __name__ == "__main__":
    main()