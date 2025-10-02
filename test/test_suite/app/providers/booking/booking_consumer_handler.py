from typing import cast
from hotel_info_lib import (
    TaskProcessorConsumer,
    RequestResponse,
    ParsedData,
    ProcessRequestParsingTask,
    ExecutionNodeStateResultEnum,
    log
)
from sqlalchemy.orm import Session
from .consumers import BookingPriceConsumer, BookingHotelInfoConsumer, BookingHotelPromotionsConsumer

class BookingConsumerHandler(TaskProcessorConsumer):
    
    def __init__(self, db: Session):
        super().__init__(db)
        self.hotel_info_consumer = BookingHotelInfoConsumer(db)
        self.price_consumer = BookingPriceConsumer(db)
        self.promotion_consumer = BookingHotelPromotionsConsumer(db)
    
    
    def _get_consumer_for_task_type(self, task_type: str):
        """Route to the appropriate consumer based on task type"""
        consumers = {
            "HOTEL_INFO": self.hotel_info_consumer,
            "HOTEL_PRICES": self.price_consumer,
            "HOTEL_PROMOTIONS": self.promotion_consumer,
        }
        
        consumer = consumers.get(task_type)
        if not consumer:
            raise ValueError(f"No consumer found for task type: {task_type}")
        
        return consumer

    def do_request(self, task: ProcessRequestParsingTask) -> RequestResponse:
        try:
            task_type = cast(str, task.task_type)
            log(log_path="app/booking_consumer_handler.py | BookingConsumerHandler/do_request", individual_id=cast(int, task.task_id), log_message=f"Routing to {task_type} consumer", log_level="INFO")
            
            consumer = self._get_consumer_for_task_type(task_type)
            return consumer.do_request(task)
            
        except (ValueError, AttributeError, TypeError, KeyError) as e:
            log(log_path="app/booking_consumer_handler.py | BookingConsumerHandler/do_request", individual_id=cast(int, task.task_id), log_message=f"Error in generic consumer routing: {e}", log_level="ERROR")
            return RequestResponse(
                data={"error": "Failed to route request", "details": str(e)},
                result=ExecutionNodeStateResultEnum.FAILED
            )

    def parse_response(self, response: RequestResponse, task: ProcessRequestParsingTask) -> ParsedData:
        try:
            task_type = cast(str, task.task_type)
            log(log_path="app/booking_consumer_handler.py | BookingConsumerHandler/parse_response", individual_id=cast(int, task.task_id), log_message=f"Routing parsing to {task_type} consumer", log_level="INFO")
            
            consumer = self._get_consumer_for_task_type(task_type)
            return consumer.parse_response(response, task)
            
        except (ValueError, AttributeError, TypeError, KeyError) as e:
            log(log_path="app/booking_consumer_handler.py | BookingConsumerHandler/parse_response", individual_id=cast(int, task.task_id), log_message=f"Error in generic consumer parsing: {e}", log_level="ERROR")
            return ParsedData(data=None, result=ExecutionNodeStateResultEnum.FAILED, sold_out_hotel=False) 