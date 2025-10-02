from typing import cast, Any
from hotel_info_lib import ProcessRequestParsingTask, RequestParameters, RequestTypeEnum, LocationEnum, Request, log
from ..booking_config import get_booking_config

def booking_url_executor(task : ProcessRequestParsingTask) -> dict[str, Any]:
    successfully_scraped = False
    scraped_data = None
    url = None
    try:
        config = get_booking_config(task)
        
        # Parse cookie string into dictionary format
        cookie_str = config['cookie']
        cookies_dict: dict[str, str] = {}
        if cookie_str:
            # Extract the first key=value pair before any semicolon
            cookie_part = cookie_str.split(';')[0]
            if '=' in cookie_part:
                key, value = cookie_part.split('=', 1)
                cookies_dict[key] = value
        
        params = RequestParameters(
            url=config['url'],
            headers=config['headers'],
            location=cast(LocationEnum, task.task__parsing_variables_region), # type: ignore
            request_type=RequestTypeEnum.GET,
            params={},
            cookies=cookies_dict       
        )
        
        request = Request(params=params)
        
        response = request.curl_request_api_get()
        
        log(saving_data=response, saving_path="debug/responses/init_response_executor.html") # type: ignore

        if not response:
            raise (ValueError)("Request failed")
        else:
            successfully_scraped = True
            scraped_data = response
            url = config['url']
    except (ValueError, AttributeError, TypeError, KeyError) as e:
        successfully_scraped = False
        log(log_message=f"Error scraping booking.com: {e}", log_path="app/booking_executor.py | booking_executor", individual_id=cast(int, task.task_id), log_level="ERROR" )
    
    return {
            "successfully_scraped": successfully_scraped,
            "scraped_data": {
                "url" : url,
                "data" : scraped_data
            }
        }
    
    