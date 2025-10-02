#!/usr/bin/env python3
"""
Test script for RMQConsumer - demonstrates usage across multiple applications.

This script creates 'test' and 'test.dlq' queues and shows how to:
1. Initialize RMQConsumer with custom configuration
2. Run multiple consumer instances in parallel
3. Configure workers, prefetch, and DB connections per consumer
4. Handle graceful shutdown

Usage:
    python test.py
"""

import multiprocessing
import signal
import sys
import time
from typing import Any, Dict, List

# Import your TaskProcessorConsumer implementation
# from your_app.consumers import YourTaskProcessorConsumer
from hotel_info_lib.consumers.rmq_consumer import RMQConsumer
from hotel_info_lib.consumers.task_processor_consumer import TaskProcessorConsumer
from hotel_info_lib.logging import log


# Example TaskProcessorConsumer implementation for testing
class TestTaskProcessorConsumer(TaskProcessorConsumer):
    """Example implementation of TaskProcessorConsumer for testing."""

    def handler(self, task: Any) -> None:
        """Process the task - replace with your actual logic."""
        task_id = getattr(task, "id", "unknown")
        log(
            log_path="TestTaskProcessor",
            log_message=f"Processing task {task_id}",
            log_level="INFO",
        )

        # Simulate some work
        time.sleep(0.1)

        log(
            log_path="TestTaskProcessor",
            log_message=f"Completed task {task_id}",
            log_level="INFO",
        )


def run_consumer_instance(consumer_id: int, config: Dict[str, Any]) -> None:
    """Run a single consumer instance in a separate process."""

    # Initialize consumer for this process
    consumer = RMQConsumer(
        processor_consumer_class=TestTaskProcessorConsumer,
        rabbitmq_url=config["rabbitmq_url"],
        queue_name=config["queue_name"],
        max_workers=config["max_workers"],
        max_db_connections=config["max_db_connections"],
        prefetch_count=config["prefetch_count"],
    )

    def signal_handler(signum: int, frame: Any) -> None:
        """Handle shutdown signals gracefully."""
        log(
            log_path=f"test.py/consumer-{consumer_id}",
            log_message="Received shutdown signal",
            log_level="INFO",
        )
        sys.exit(0)

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        log(
            log_path=f"test.py/consumer-{consumer_id}",
            log_message=f"Starting consumer {consumer_id} - Workers: {config['max_workers']}, Prefetch: {config['prefetch_count']}",
            log_level="INFO",
        )

        # Only initialize queues on the first consumer to avoid conflicts
        if consumer_id == 1:
            consumer.initialize()

            # Optional: Purge existing messages from queue (uncomment if needed)
            # consumer.purge_queue()

            log(
                log_path=f"test.py/consumer-{consumer_id}",
                log_message="Queues initialized. Ready to receive messages.",
                log_level="INFO",
            )
        else:
            # Other consumers just need connection, queues already exist
            try:
                consumer._setup_connection()  # type: ignore[misc]
            except:
                # Fallback: try full initialization if connection fails
                consumer.initialize()

        # Start consuming messages
        consumer.start_consuming()

    except KeyboardInterrupt:
        log(
            log_path=f"test.py/consumer-{consumer_id}",
            log_message="Interrupted by user",
            log_level="INFO",
        )
    except Exception as e:
        log(
            log_path=f"test.py/consumer-{consumer_id}",
            log_message=f"Error: {e}",
            log_level="ERROR",
        )
        raise
    finally:
        log(
            log_path=f"test.py/consumer-{consumer_id}",
            log_message=f"Consumer {consumer_id} stopped",
            log_level="INFO",
        )


def main():
    """Main test function - runs multiple consumer instances."""

    # ============================================================================
    # CONSUMER CONFIGURATION
    # ============================================================================
    NUM_CONSUMERS = 5  # Number of consumer instances to run
    WORKERS_PER_CONSUMER = 4  # Workers per consumer (total: 5 x 4 = 20 workers)
    PREFETCH_PER_CONSUMER = 10  # Messages prefetched per consumer
    DB_CONNECTIONS_PER_CONSUMER = (
        20  # DB connections per consumer (total: 5 x 20 = 100)
    )

    RABBITMQ_URL = "amqp://admin:admin@localhost:5672/"
    QUEUE_NAME = "test"

    # ============================================================================

    config = {
        "rabbitmq_url": RABBITMQ_URL,
        "queue_name": QUEUE_NAME,
        "max_workers": WORKERS_PER_CONSUMER,
        "max_db_connections": DB_CONNECTIONS_PER_CONSUMER,
        "prefetch_count": PREFETCH_PER_CONSUMER,
    }

    log(
        log_path="test.py",
        log_message=f"Starting {NUM_CONSUMERS} consumer instances - "
        f"Total workers: {NUM_CONSUMERS * WORKERS_PER_CONSUMER}, "
        f"Total prefetch: {NUM_CONSUMERS * PREFETCH_PER_CONSUMER}, "
        f"Total DB connections: {NUM_CONSUMERS * DB_CONNECTIONS_PER_CONSUMER}",
        log_level="INFO",
    )

    # Start consumer processes
    processes: List[multiprocessing.Process] = []

    try:
        for i in range(1, NUM_CONSUMERS + 1):
            process = multiprocessing.Process(
                target=run_consumer_instance, args=(i, config), name=f"Consumer-{i}"
            )
            process.start()
            processes.append(process)
            log(
                log_path="test.py",
                log_message=f"Started consumer process {i} (PID: {process.pid})",
                log_level="INFO",
            )

        # Wait for all processes to complete
        for process in processes:
            process.join()

    except KeyboardInterrupt:
        log(
            log_path="test.py",
            log_message="Interrupted by user - stopping all consumers",
            log_level="INFO",
        )

        # Terminate all consumer processes
        for process in processes:
            if process.is_alive():
                log(
                    log_path="test.py",
                    log_message=f"Terminating consumer process {process.name} (PID: {process.pid})",
                    log_level="INFO",
                )
                process.terminate()
                process.join(timeout=5)

                # Force kill if still alive
                if process.is_alive():
                    process.kill()
                    process.join()

        log(
            log_path="test.py",
            log_message="All consumer processes stopped",
            log_level="INFO",
        )

    except Exception as e:
        log(log_path="test.py", log_message=f"Error in main: {e}", log_level="ERROR")
        raise


def test_bulk_publish():
    """Test function to publish multiple messages for load testing."""

    RABBITMQ_URL = "amqp://admin:admin@localhost:5672/"
    QUEUE_NAME = "test"

    consumer = RMQConsumer(
        processor_consumer_class=TestTaskProcessorConsumer,
        rabbitmq_url=RABBITMQ_URL,
        queue_name=QUEUE_NAME,
    )

    try:
        consumer.initialize()

        # Publish 100 test messages for stress testing
        log(
            log_path="test.py",
            log_message="Publishing 100 test messages...",
            log_level="INFO",
        )

        for i in range(1, 101):
            consumer.publish_test_message(2000 + i)
            if i % 20 == 0:
                log(
                    log_path="test.py",
                    log_message=f"Published {i} messages",
                    log_level="INFO",
                )

        log(
            log_path="test.py",
            log_message="Finished publishing test messages",
            log_level="INFO",
        )

    except Exception as e:
        log(
            log_path="test.py",
            log_message=f"Error publishing messages: {e}",
            log_level="ERROR",
        )
        raise
    finally:
        pass


if __name__ == "__main__":
    # Choose which function to run:

    # 1. Start the consumer (main usage)
    main()

    # 2. Or just publish test messages for load testing
    # test_bulk_publish()
