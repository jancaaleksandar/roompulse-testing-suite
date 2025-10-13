import json
from http.client import responses
import os
import re
import requests
from ..test_suite.app.providers.google.common.clean_response_common import  CleanResponse
from ..test_suite.app.providers.google.parsers.place_parser import SinglePlaceParser

def test_proxy(proxy_url : str) -> None:
    proxies = {"http": proxy_url, "https": proxy_url}
    # target_url = "https://www.google.com/maps/place/data=!4m11!3m10!1s0x14a1bbada8ec898f:0xf42dbcec3657f977!5m2!4m1!1i2!8m2!3d37.9396556!4d23.6615008!16s%2Fg%2F11h5x9z_fq"
    target_url = f"https://www.google.com/maps/place/data=!4m11!3m10!1s0x14a1bbada8ec898f:0xf42dbcec3657f977!5m4!1s2025-12-21!2i3!4m1!1i2!8m2!3d00.0000000!4d00.0000000!16s?ucbcb=1&entry=ttu"
    response = requests.get(url=target_url, proxies=proxies, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}, verify=False)
    print(f"Status code: {response.status_code} - {responses[response.status_code]}")
    
    # Create debug directory if it doesn't exist
    debug_dir = "test/random/debug"
    os.makedirs(debug_dir, exist_ok=True)
    
    # Sanitize the proxy URL to create a valid filename
    # Replace invalid characters with underscores
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', proxy_url)
    # Also replace @ with _ for better readability
    safe_filename = safe_filename.replace('@', '_at_')
    
    file_path = os.path.join(debug_dir, f"{safe_filename}.json")
    

    print(f"Response saved to: {file_path}")
    cleaner_response = CleanResponse(response=response.text).clean_response()
    with open(file_path, "w") as f:
        json.dump(cleaner_response, f, indent=4)

    parsed_response = SinglePlaceParser(response=cleaner_response["data"]).get_place_details()
    print(f"Parsed response: {parsed_response}")


if __name__ == "__main__" :
    # target_proxy = "http://z3et3mrlv18axyhf5heid7:rbf9la12klj2e7fc0xxr34@scrapoxy.roompulse.internal:8888 " # australia
    target_proxy = "http://obc54l60asl2hw3ef8cfwy:chp0pm7ruvl57gnhz1tn@scrapoxy.roompulse.internal:8888" # canada
    # target_proxy = "http://u5cfakq7sclif2qixsdp:xf0rtgbsb88ny48mmnh3h@scrapoxy.roompulse.internal:8888" # ireland
    # target_proxy = "http://tannt6eelmfdt0vrlvfpq:7jdz038ibr2px26t50b6m@scrapoxy.roompulse.internal:8888" # israel

    test_proxy(target_proxy)