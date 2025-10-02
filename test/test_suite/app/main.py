import secrets

from .execute_all_requests import execute_all_requests
from .parameter_generator import ParameterGenerator
from .processor import Processor
from .types import UserInput


def main(client_input: list[UserInput]) -> None:
    try:
        run_id = secrets.randbelow(9000000) + 1000000
        print(f"🚀 Starting test run {run_id} with {len(client_input)} requests...")

        # get_bm_s_cookie = get_bm_s_cookie()

        parameter_generator = ParameterGenerator(client_input=client_input)
        request_parameters = parameter_generator.generate_request_parameters()

        all_run_requests = execute_all_requests(request_parameters=request_parameters, max_workers=30)
        print(f"✅ Processed {len(all_run_requests)} total requests (including retries)")

        processor = Processor(all_run_requests=all_run_requests, run_id=run_id)
        processor.save_run()
        print(f"💾 Results saved to run_summary/{run_id}/")

    except (ValueError, TypeError, RuntimeError, OSError) as e:
        print(f"❌ Error in main: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    import datetime

    client_inputs: list[UserInput] = []
    num_requests = 10  # Create 10 requests for testing

    for _ in range(num_requests):
        # Randomize check-in date (from tomorrow to 1 year in the future)
        today = datetime.date.today()
        random_days_in_future = secrets.randbelow(365) + 1
        check_in_date = today + datetime.timedelta(days=random_days_in_future)

        # Randomize nights (from 1 to 5)
        nights = secrets.randbelow(5) + 1

        user_input = UserInput(
            provider_id="38235667",
            request_check_in_date=check_in_date.strftime("%Y-%m-%d"),
            request_nights=nights,
            request_currency="USD",
            request_adults=2,
            # request_proxies="http://92xi5qybn9op057cysfxu9:m1oc0vhp7gagrglsyjhk@scrapoxy.roompulse.internal:8888",
            request_proxy="http://w4l5227ces9ijsa6w8uipm:a3ojfg0nwwxq8obozlg1@scrapoxy.roompulse.internal:8888",
            request_request_type="POST",
            request_provider="EXPEDIA",
            request_maximum_retries=1,
            request_type="PROXY_TESTING",
        )
        print(user_input)
        client_inputs.append(user_input)

    main(client_input=client_inputs)
