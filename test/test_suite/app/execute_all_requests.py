from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from threading import Lock
from .types import RequestParameters, RunRequest
from .providers.expedia.expedia_request import expedia_request







def execute_all_requests(request_parameters: list[RequestParameters], max_workers: int = 1) -> list[RunRequest]:
    """Execute all requests using multithreading with configurable number of workers"""
    all_run_requests: list[RunRequest] = []
    request_counter = 0
    
    # Thread-safe lock for progress reporting
    progress_lock = Lock()
    completed_requests = 0
    total_requests = len(request_parameters)
    
    print(f"🚀 Starting {total_requests} requests with {max_workers} workers...")
    
    # Create a list of (params, request_id) tuples
    tasks: list[tuple[RequestParameters, int]] = []
    for params in request_parameters:
        request_counter += 1
        tasks.append((params, request_counter))
    
    # Use ThreadPoolExecutor to process requests in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_task: dict[Future[list[RunRequest]], tuple[RequestParameters, int]] = {
            executor.submit(expedia_request, params, request_id): (params, request_id)
            for params, request_id in tasks
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_task.keys()):
            params, request_id = future_to_task[future]
            
            try:
                # Get the result from the completed future
                run_requests = future.result()
                all_run_requests.extend(run_requests)
                
                # Thread-safe progress reporting
                with progress_lock:
                    completed_requests += 1
                    if completed_requests % 10 == 0 or completed_requests == total_requests:
                        print(f"📊 Progress: {completed_requests}/{total_requests} requests completed")
                        
            except (ValueError, Exception) as e:
                print(f"❌ Fatal error processing request {request_id}: {e}")
                # Continue to next request even if this one completely fails
                with progress_lock:
                    completed_requests += 1
                continue
    
    print(f"✅ All {total_requests} requests completed!")
    return all_run_requests