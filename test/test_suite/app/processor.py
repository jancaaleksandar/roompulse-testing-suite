from datetime import datetime
import json
from pathlib import Path
from typing import Any

from .types import RunRequest


class Processor:
    def __init__(self, all_run_requests: list[RunRequest], run_id: int) -> None:
        self.run_id = run_id
        self.all_run_requests = all_run_requests
        self.directories = self._initialize_all_response_directories()

    def _initialize_all_response_directories(self) -> dict[str, Path]:
        # Create directories if they don't exist, do nothing if they do
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_summary_dir = Path(f"test/test_suite/output/run_summary/{self.run_id}_{timestamp}")
        requests_dir = Path(f"{run_summary_dir}/requests")
        responses_dir = Path(f"{run_summary_dir}/responses")

        requests_dir.mkdir(parents=True, exist_ok=True)
        responses_dir.mkdir(parents=True, exist_ok=True)
        run_summary_dir.mkdir(parents=True, exist_ok=True)

        return {"requests_dir": requests_dir, "responses_dir": responses_dir, "run_summary_dir": run_summary_dir}

    def _generate_md_file(self) -> None:
        # Calculate statistics
        total_attempts = len(self.all_run_requests)  # This includes retries
        if total_attempts == 0:
            return

        # Get unique initial requests (count unique request_ids)
        unique_request_ids = set(req["request_id"] for req in self.all_run_requests)
        initial_requests = len(unique_request_ids)

        # Calculate total retries performed across all requests
        # Retries = Total attempts - Initial requests (since each request gets at least 1 initial attempt)
        total_retries_performed = total_attempts - initial_requests

        # Time calculations
        total_time = sum(float(req["request_time"]) for req in self.all_run_requests)

        # Success calculations - only count successful attempts
        successful_attempts = [req for req in self.all_run_requests if req["request_successful"]]
        total_successful_attempts = len(successful_attempts)

        # Calculate successful unique requests (unique request_ids that had at least one success)
        successful_request_ids = set(req["request_id"] for req in successful_attempts)
        total_success_requests = len(successful_request_ids)

        # Failed requests (unique request_ids that never succeeded)
        total_failed_requests = initial_requests - total_success_requests

        # Average time per attempt (including retries)
        average_time_per_attempt = total_time / max(total_attempts, 1)

        # Status code analysis - count ALL attempts
        status_codes: dict[str, int] = {}
        for req in self.all_run_requests:
            status_code = str(req["request_status_code"])
            status_codes[status_code] = status_codes.get(status_code, 0) + 1

        # Generate markdown content
        md_content = f"""# Test Run Summary - {self.run_id}

## Overview
- **Run ID**: {self.run_id}
- **Total Initial Requests**: {initial_requests}
- **Total Attempts (including retries)**: {total_attempts}
- **Total Retries Performed**: {total_retries_performed}
- **Total Time**: {total_time:.2f} seconds
- **Average Time per Attempt**: {average_time_per_attempt:.4f} seconds

## Results Summary
- **Successful Requests**: {total_success_requests} out of {initial_requests} ({(total_success_requests / initial_requests * 100):.1f}%)
- **Failed Requests**: {total_failed_requests} out of {initial_requests} ({(total_failed_requests / initial_requests * 100):.1f}%)

## Status Code Breakdown (All Attempts)
"""

        # Add status code breakdown with cleaner format
        for status_code, count in sorted(status_codes.items()):
            percentage = count / total_attempts * 100
            md_content += f"- **{status_code}**: {count} times ({percentage:.1f}%)\n"

        md_content += f"""
## Performance Details
- **Fastest Attempt**: {min(float(req["request_time"]) for req in self.all_run_requests):.4f}s
- **Slowest Attempt**: {max(float(req["request_time"]) for req in self.all_run_requests):.4f}s
- **Most Retries for Single Request**: {max(req["request_retries"] for req in self.all_run_requests)}
- **Average Retries per Request**: {total_retries_performed / initial_requests:.2f}

## Additional Info
- **Unique URLs Tested**: {len(set(req["request_url"] for req in self.all_run_requests))}
- **Total Successful Attempts**: {total_successful_attempts} out of {total_attempts}
"""

        # Save to file
        md_file_path = self.directories["run_summary_dir"] / "run_summary.md"
        with open(md_file_path, "w") as f:
            f.write(md_content)

    def _generate_run_json_file(self) -> None:
        """Generate a comprehensive JSON file with all request details"""

        # Create the main run overview structure
        requests_list: list[dict[str, Any]] = []

        # Process each request
        for req in self.all_run_requests:
            # Format proxy information
            proxy_info = f"{req['request_proxy']}"

            request_entry: dict[str, Any] = {
                "request_id": req["request_id"],
                "url": req["request_url"],
                "retries": req["request_retries"],
                "time": req["request_time"],
                "status": req["request_status_code"],
                "proxy": proxy_info,
                "successful": req["request_successful"],
                "fingerprint": req.get("request_fingerprint", None),
            }

            requests_list.append(request_entry)

        run_overview: dict[str, Any] = {
            "run_id": self.run_id,
            "total_requests": len(self.all_run_requests),
            "requests": requests_list,
        }

        # Save to file
        json_file_path = self.directories["run_summary_dir"] / "run_overview.json"
        with open(json_file_path, "w") as f:
            json.dump(run_overview, f, indent=2)

    def _save_requests_debug_details(self) -> None:
        """Save detailed debug information for each individual request"""

        for req in self.all_run_requests:
            request_id = req["request_id"]

            # Create detailed request data structure
            request_debug_data = {
                "request_id": request_id,
                "request_url": req["request_url"],
                "request_retries": req["request_retries"],
                "request_headers": req.get("request_headers", {}),
                "request_time": req["request_time"],
                "request_status_code": req["request_status_code"],
                "request_successful": req["request_successful"],
                "request_proxy": req["request_proxy"],
                "request_fingerprint": req.get("request_fingerprint", None),
                "response_data": req["response"],
            }

            # Save request debug data
            request_file_path = (
                self.directories["requests_dir"]
                / f"request_{request_id}_{req['request_retries']}_{req['request_status_code']}_{req['request_successful']}.json"
            )
            with open(request_file_path, "w") as f:
                json.dump(request_debug_data, f, indent=2, default=str)

    def _save_responses_debug_details(self) -> None:
        for req in self.all_run_requests:
            request_id = req["request_id"]
            response_file_path = (
                self.directories["responses_dir"]
                / f"response_{request_id}_{req['request_retries']}_{req['request_status_code']}_{req['request_successful']}.json"
            )
            with open(response_file_path, "w") as f:
                json.dump(req["response"], f, indent=2, default=str)

    def save_run(self) -> None:
        """Save the test run data and generate summary files"""
        self._generate_md_file()
        self._generate_run_json_file()
        self._save_requests_debug_details()
        self._save_responses_debug_details()
