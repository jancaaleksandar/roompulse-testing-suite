from typing import Any, cast
from hotel_info_lib import TaskProcessorConsumer, ProcessRequestParsingTask, RequestResponse, ExecutionNodeStateResultEnum, ParsedData, log, RawHotelInfoCreate
from ..executors.booking_url_executor import booking_url_executor
from ..parsers.booking_hotel_info_parser import BookingHotelInfoParser
from ..utils.raw_hotel_info_mapping import booking_raw_hotel_info_mapper

class BookingHotelInfoConsumer(TaskProcessorConsumer):
    
    def do_request(self, task: ProcessRequestParsingTask) -> RequestResponse:
        response_data: dict[str, Any] = booking_url_executor(task=task)
        if not response_data.get("successfully_scraped"):
            return RequestResponse(
                data={"error": "Failed to scrape all rooms", "details": response_data.get("response")},
                result=ExecutionNodeStateResultEnum.FAILED
            )
        return RequestResponse(
            data=response_data.get("scraped_data"),
            result=ExecutionNodeStateResultEnum.SUCCESS
        )
    
    def parse_response(self, response: RequestResponse, task: ProcessRequestParsingTask) -> ParsedData: # type: ignore
        if response.result == ExecutionNodeStateResultEnum.FAILED or not response.data:
            error_details = response.data if response.data else "No data from failed request (or request itself failed)"
            log(log_path="BookingPriceConsumer/parse_response", individual_id=cast(int, task.task_id), log_message=f"Skipping parsing: {error_details}", log_level="ERROR")
            return ParsedData(data=None, result=ExecutionNodeStateResultEnum.FAILED, sold_out_hotel=False)
        
        response_dict = cast(dict[str, Any], response.data)
        url = response_dict.get("url")
        data = response_dict.get("data")
        
        if not url or not data:
            log(log_path="app/consumers/booking_hotel_info_consumer.py | BookingHotelInfoConsumer/parse_response", individual_id=cast(int, task.task_id), log_message="No url or data in response", log_level="ERROR")
            return ParsedData(data=None, result=ExecutionNodeStateResultEnum.FAILED, sold_out_hotel=False)
        
        parser = BookingHotelInfoParser(response=cast(str, data), task=task)
        parsed_data = parser.parse()
        
        if not parsed_data["successfully_parsed"]:
            return ParsedData(data=None, result=ExecutionNodeStateResultEnum.FAILED, sold_out_hotel=False)
        log(saving_data=parsed_data, saving_path="debug/responses/parsed_hotel_info.json") # type: ignore
        
        raw_hotel_info_list: list[RawHotelInfoCreate] = booking_raw_hotel_info_mapper(hotel_info=parsed_data["hotel_info"], task=task , url=url)
        
        return ParsedData(data=raw_hotel_info_list, result=ExecutionNodeStateResultEnum.SUCCESS, sold_out_hotel=False)