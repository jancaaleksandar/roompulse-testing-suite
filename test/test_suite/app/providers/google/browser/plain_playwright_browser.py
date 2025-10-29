from typing import TypedDict
from playwright.sync_api import Playwright, sync_playwright


class ProxyStructureType(TypedDict):
    host: str
    port: int
    username: str
    password: str


def plain_playwright_browser_testing(playwright_initiated: Playwright, proxy: ProxyStructureType) -> None:
    print("-" * 50)
    print("STARTING PLAIN PLAYWRIGHT TESTING")
    print("-" * 50)

    # Configure proxy settings for Playwright
    proxy_config : ProxySettings = {
        "server": f"http://{proxy['host']}:{proxy['port']}",
        "username": proxy["username"],
        "password": proxy["password"]
    }
    print(f"DEBUG : got proxy config : {proxy_config}")

    # Launch browser with proxy configuration
    chromium = playwright_initiated.chromium
    print("DEBUG : got chromium")
    
    browser = chromium.launch(
        headless=False,  # Set to False to see the browser
        proxy=proxy_config
    )
    print("DEBUG : got browser")
    
    # Create a new context and page
    context = browser.new_context()
    print("DEBUG : got context")
    
    page = context.new_page()
    print("DEBUG : got page")

    try:
        print("DEBUG : trying to go to the page")
        page.goto(
            # url="https://www.booking.com",
            # url="https://www.google.com/maps",
            url="https://www.google.com/maps/place/Best+Western+Plus+Philadelphia-Pennsauken+Hotel/@39.9347213,-75.0755581,16.57z/data=!4m11!3m10!1s0x89c6c96eba3e2c85:0xc420d3f9c9e9c59e!5m4!1s2025-12-21!2i3!4m1!1i2!8m2!3d39.93363!4d-75.07762!16s%2Fg%2F11fcttw9y1?entry=ttu&g_ep=EgoyMDI1MTAwOC4wIKXMDSoASAFQAw%3D%3D",
            wait_until="domcontentloaded",
            timeout=120000
        )
        print("DEBUG : page loaded")

        # Click "Accept all" button if it appears
        try:
            print("DEBUG : looking for 'Accept all' button")
            # Wait for the button to appear
            accept_button = page.locator("button:has-text('Accept all')").first
            accept_button.wait_for(state="visible", timeout=10000)
            print("DEBUG : 'Accept all' button is visible")
            
            # Click and wait for navigation to complete
            with page.expect_navigation(wait_until="domcontentloaded", timeout=30000):
                accept_button.click()
            print("DEBUG : clicked 'Accept all' button and navigation completed")
            
            # Wait for the page to stabilize after consent
            page.wait_for_load_state("networkidle", timeout=30000)
            print("DEBUG : page stabilized after consent")
        except Exception as e:
            print(f"DEBUG : 'Accept all' button not found or couldn't click: {e}")

        # Save HTML content
        html_content = page.content()
        with open(f"test/test_suite/app/providers/google/debug/plain_playwright_html_{proxy['host']}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("DEBUG : html content saved")

        # Optional: wait for additional content to load
        page.wait_for_timeout(3000)  # Wait 3 seconds for dynamic content
        
        page.screenshot(path=f"test/test_suite/app/providers/google/debug/plain_playwright_screenshot_{proxy['host']}.png")
        print("DEBUG : screenshot taken")
    except Exception as e:
        print(f"ERROR : {e}")
    finally:
        page.close()
        context.close()
        browser.close()
        print("Session complete!")


def main() -> None:
    with sync_playwright() as playwright:
        # proxy: ProxyStructureType = {
        #     "host": "scrapoxy.roompulse.internal",
        #     "port": 8888,
        #     "username": "kxvkzxpqtsvlbppsnkkfs",
        #     "password": "ghjvta8ohh9qvgklicep1"
        # }
        # proxy: ProxyStructureType = {
        #     "host": "scrapoxy.roompulse.internal",
        #     "port": 8888,
        #     "username": "obc54l60asl2hw3ef8cfwy",
        #     "password": "chp0pm7ruvl57gnhz1tn"
        # }
                # "proxy_host": "202.68.181.43",

        #  working us iproyal
        # proxy: ProxyStructureType = {
        #     "host": "88.216.46.37",
        #     "port": 12323,
        #     "username": "14ab59fe1cc10",
        #     "password": "07c7b5a1e1"
        # }
        proxy: ProxyStructureType = {
        "host": "51.159.157.219",
        "port": 9000,
        "username": "geonode_lMtU7NlVhq-country-us",
        "password": "6cab342c-0f28-4635-9573-2ea5c7867313"
        }

        # proxy: ProxyStructureType = {
        #     "host": "51.159.157.219",
        #     "port": 9000,
        #     "username": "geonode_lMtU7NlVhq-country-tr",
        #     "password": "6cab342c-0f28-4635-9573-2ea5c7867313",
        # }

        plain_playwright_browser_testing(playwright, proxy)


if __name__ == "__main__":
    main()