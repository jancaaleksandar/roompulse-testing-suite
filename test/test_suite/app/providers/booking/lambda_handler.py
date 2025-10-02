import json

from hotel_info_lib import log  # type: ignore
# from ...database import force_close_all_connections
from .consumers.booking_price_consumer import BookingPriceConsumer
from sqlalchemy.orm import Session
from typing import Any, Dict
from hotel_info_lib.database.database_manager import create_database_connection, dispose_engine
from hotel_info_lib.consumers.lambda_consumer import LambdaConsumer # Import the new LambdaConsumer


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for processing SQS messages sequentially.
    Uses LambdaConsumer to process each message with a specific TaskProcessorConsumer.
    """
    try:
        messages = event.get('Records', [])
        if not messages:
            return {
                "statusCode": 200,
                "body": json.dumps({"processedMessages": 0, "status": "No messages to process"})
            }
            
        db_session: Session | None = create_database_connection()
        # Process messages sequentially
        for index, message_body in enumerate(messages):
            # db_session is created for each message now inside process_each_message
            process_single_message_with_consumer(message_body, index, len(messages), db_session)

        return {
            "statusCode": 200,
            "body": json.dumps({"status": f"Attempted processing for {len(messages)} messages"})
        }

    except Exception as e:
        error_msg = f"Lambda handler level error: {str(e)}"
        log(log_path="lambda_handler", log_message=error_msg, log_level="ERROR")
        return {
            "statusCode": 500, # Indicate a handler-level failure
            "body": json.dumps({"error": error_msg, "status": "Handler failed"})
        }
    finally:
        try:
            dispose_engine()
            log(log_path="lambda_handler", log_message="Disposed database engine.", log_level="INFO")
        except Exception as dispose_error:
            log(log_path="lambda_handler", log_message=f"Error disposing engine: {dispose_error}", log_level="ERROR")


def process_single_message_with_consumer(message_body: dict[str, Any], index: int, total_messages: int, db_session: Session) -> None:
    """
    Helper function to process a single message.
    Creates a DB session, then uses LambdaConsumer to instantiate and run the appropriate TaskProcessorConsumer.
    """
    message_id_for_log = message_body.get('messageId', f'unknown-{index}') # For logging if session fails
    log(log_path="process_single_message", individual_id=message_id_for_log, log_message=f"Starting processing of message {index+1}/{total_messages}", log_level="INFO")

    try:
        # Instantiate LambdaConsumer, passing the AgodaConsumer CLASS and the session
        # LambdaConsumer will then instantiate AgodaConsumer(db=db_session) internally.
        lambda_orchestrator = LambdaConsumer(processor_consumer_class=BookingPriceConsumer, db=db_session)
        
        # Pass the raw SQS message_body to LambdaConsumer's handler
        lambda_orchestrator.handler(message_body)
        db_session.commit()
        log(log_path="process_single_message", individual_id=message_id_for_log, log_message=f"Successfully processed and committed message {message_id_for_log}", log_level="INFO")

    except Exception as e:
        # This catches errors from LambdaConsumer.handler (which includes errors from AgodaConsumer.handler if re-raised)
        # or errors during db_session.commit() if processing seemed successful before commit.
        error_msg = f"Error processing message {message_id_for_log}: {e}"
        log(log_path="process_single_message", individual_id=message_id_for_log, log_message=error_msg, log_level="ERROR")
        if db_session: # Attempt rollback if session exists
            try:
                db_session.rollback()
                log(log_path="process_single_message", individual_id=message_id_for_log, log_message="Transaction rolled back due to error.", log_level="WARN")
            except Exception as rollback_error:
                log(log_path="process_single_message", individual_id=message_id_for_log, log_message=f"Error during rollback: {rollback_error}", log_level="ERROR")
    finally:
        if db_session:
            try:
                db_session.close()
                log(log_path="process_single_message", individual_id=message_id_for_log, log_message="DB session closed.", log_level="INFO")
            except Exception as close_error:
                log(log_path="process_single_message", individual_id=message_id_for_log, log_message=f"Error closing DB session: {close_error}", log_level="ERROR")