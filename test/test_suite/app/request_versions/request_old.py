# from ...app_config import get_config
# from curl_cffi import requests
# import json
# import time
# import random
# from .http_proxy import get_proxy
# from ...logging import log
# from ...common.common_get_proxy_ip import get_proxy_ip
# from curl_cffi.const import CurlOpt
# from curl_cffi.requests import ExtraFingerprints


# SIG_ALG_POOL = [
#     "ecdsa_secp256r1_sha256", "ecdsa_secp384r1_sha384",
#     "rsa_pss_rsae_sha256",    "rsa_pss_rsae_sha512",
#     "rsa_pkcs1_sha256",       "rsa_pkcs1_sha512",
# ]

# # Capability checks
# FP_FIELDS = ExtraFingerprints.__dataclass_fields__.keys()
# HAS_disable_sigs = "tls_disable_sigs" in FP_FIELDS
# HAS_akamai_fp = "akamai" in FP_FIELDS
# HAS_session_ticket_disable = "tls_session_ticket_disable" in FP_FIELDS

# H2_PRESETS = [
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=1000,MAX_HEADER_LIST_SIZE=262144",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=131072,"
#     "MAX_CONCURRENT_STREAMS=100,MAX_HEADER_LIST_SIZE=32768",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=200,MAX_HEADER_LIST_SIZE=262144",
# ]


# AKAMAI_PRESETS = [
#     "|10485760|0|m,s,p,a",
#     "|15663105|0|m,a,s,p",
#     "|11534336|0|m,p,a,s",
#     "|14680064|0|s,m,p,a",
# ]


# def make_request(params, max_retries=25) -> dict:
#     """
#     Make a request to the API with retry logic and proxy support.

#     Args:
#         params: Request parameters
#         max_retries: Maximum number of retry attempts

#     Returns:
#         dict: Response data with success indicator. Always includes 'success' key.
#               If successful: {'success': True, 'data': response_data, ...}
#               If failed: {'success': False, 'error': error_message, 'retries': max_retries}
#     """
#     last_error = None
#     success = False
#     response_data = None

#     for attempt in range(max_retries):
#         # Wait before retrying (skip waiting before first attempt)
#         if attempt > 0:
#             # First delay is 5 seconds, then increment by 5 seconds for each subsequent retry
#             # wait_seconds = 5 * attempt
#             # time.sleep(wait_seconds)
#             pass

#         # Reset state for this attempt
#         attempt_success = False
#         attempt_data = None

#         try:
#             # Step 1: Get config and proxy
#             config = get_config(params)

#             CURL_OPTS = {
#                 # — Kill connection reuse so every retry is a fresh fingerprint —
#                 # ← add this
#                 CurlOpt.HTTP2_SETTINGS: random.choice(H2_PRESETS),
#                 CurlOpt.FRESH_CONNECT: 1,
#                 CurlOpt.FORBID_REUSE: 1,
#             }

#             proxies = get_proxy(currency=params.task__parsing_price_variables_currency)

#             # Step 2: Make the request
#             # Build dynamic extra fingerprints for this attempt
#             sig_count = random.randint(2, len(SIG_ALG_POOL))
#             sigs = random.sample(SIG_ALG_POOL, sig_count)
#             random.shuffle(sigs)
#             fp_kwargs = dict(
#                 tls_grease=True,
#                 tls_permute_extensions=True,
#                 tls_cert_compression="brotli",
#                 tls_signature_algorithms=sigs,
#             )

#             if HAS_session_ticket_disable:
#                 # Recommended for better privacy
#                 fp_kwargs["tls_session_ticket_disable"] = True

#             if HAS_disable_sigs:
#                 # Choose 1-2 algs to drop so the *set* changes → JA4 changes
#                 drop_cnt = random.randint(1, min(2, len(sigs)-1))
#                 sigs_to_disable = random.sample(sigs, drop_cnt)
#                 fp_kwargs["tls_disable_sigs"] = sigs_to_disable

#             if HAS_akamai_fp:
#                 # Use one of the AKAMAI_PRESETS for the fingerprint
#                 fp_kwargs["akamai"] = random.choice(AKAMAI_PRESETS)

#             extra_fp = ExtraFingerprints(**fp_kwargs)

#             hdr_items = list(config["headers"].items())
#             random.shuffle(hdr_items)
#             headers = {_rand_case(k): v for k, v in hdr_items}

#             time.sleep(random.uniform(0.3, 0.8))

#             response = requests.post(
#                 config["url"],
#                 headers=headers,
#                 json=config["payload"],
#                 impersonate=config["impersonate"],   # rotate browser version
#                 extra_fp=extra_fp,                  # randomised TLS details
#                 proxies=proxies,
#                 verify=False,
#                 curl_options=CURL_OPTS,       # low-level tweaks
#             )

#             # Step 3: Process response
#             if response.status_code == 200:
#                 data = response.json()
#                 attempt_data = {
#                     "success": True,
#                     "data": data,
#                     "retries": attempt + 1,
#                 }
#                 attempt_success = True
#                 if response.status_code == 429:
#                     if params.task__parsing_price_variables_currency == "USD" or params.task__parsing_price_variables_currency == "GBP":
#                         wait = 6
#                     else:
#                         wait = int(response.headers.get("Retry-After", "2"))
#                     time.sleep(wait)
#                     continue

#                 # Force a "continue" by raising an exception that we'll catch
#                 raise Exception(f"Non-200 status code: {response.status_code}")

#         except json.JSONDecodeError as e:
#             last_error = f"JSON decode error: {str(e)}"
#             log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#                 log_message=f"Failed to parse JSON response: {str(e)}", log_level="ERROR")

#         except Exception as e:
#             last_error = str(e)


#         finally:
#             # Update overall success status from this attempt
#             if attempt_success:
#                 success = True
#                 response_data = attempt_data
#                 break  # Exit the retry loop on success

#             # Don't do anything else in finally - just proceed to next attempt

#     # After all attempts or when successful
#     if success:
#         return response_data
#     else:
#         log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#             log_message=f"Failed after {max_retries} attempts. Last error: {last_error}", log_level="ERROR")
#         return {
#             "success": False,
#             "error": last_error or "Unknown error",
#             "retries": max_retries
#         }


# def _rand_case(s):     # keep your helper handy
#     return "".join(c.upper() if random.random() < .5 else c for c in s)
# from ...app_config import get_config
# from curl_cffi import requests
# import json
# import time
# import random
# from .http_proxy import get_proxy
# from ...logging import log
# from ...common.common_get_proxy_ip import get_proxy_ip
# from curl_cffi.const import CurlOpt
# from curl_cffi.requests import ExtraFingerprints


# SIG_ALG_POOL = [
#     "ecdsa_secp256r1_sha256", "ecdsa_secp384r1_sha384",
#     "rsa_pss_rsae_sha256",    "rsa_pss_rsae_sha512",
#     "rsa_pkcs1_sha256",       "rsa_pkcs1_sha512",
# ]

# # Capability checks
# FP_FIELDS = ExtraFingerprints.__dataclass_fields__.keys()
# HAS_disable_sigs = "tls_disable_sigs" in FP_FIELDS
# HAS_akamai_fp = "akamai" in FP_FIELDS
# HAS_session_ticket_disable = "tls_session_ticket_disable" in FP_FIELDS

# H2_PRESETS = [
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=1000,MAX_HEADER_LIST_SIZE=262144",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=131072,"
#     "MAX_CONCURRENT_STREAMS=100,MAX_HEADER_LIST_SIZE=32768",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=200,MAX_HEADER_LIST_SIZE=262144",
# ]


# AKAMAI_PRESETS = [
#     "|10485760|0|m,s,p,a",
#     "|15663105|0|m,a,s,p",
#     "|11534336|0|m,p,a,s",
#     "|14680064|0|s,m,p,a",
# ]


# def make_request(params, max_retries=25) -> dict:
#     """
#     Make a request to the API with retry logic and proxy support.

#     Args:
#         params: Request parameters
#         max_retries: Maximum number of retry attempts

#     Returns:
#         dict: Response data with success indicator. Always includes 'success' key.
#               If successful: {'success': True, 'data': response_data, ...}
#               If failed: {'success': False, 'error': error_message, 'retries': max_retries}
#     """
#     last_error = None
#     success = False
#     response_data = None

#     for attempt in range(max_retries):
#         # Wait before retrying (skip waiting before first attempt)
#         if attempt > 0:
#             # First delay is 5 seconds, then increment by 5 seconds for each subsequent retry
#             # wait_seconds = 5 * attempt
#             # time.sleep(wait_seconds)
#             pass

#         # Reset state for this attempt
#         attempt_success = False
#         attempt_data = None

#         try:
#             # Step 1: Get config and proxy
#             config = get_config(params)

#             CURL_OPTS = {
#                 # — Kill connection reuse so every retry is a fresh fingerprint —
#                 # ← add this
#                 CurlOpt.HTTP2_SETTINGS: random.choice(H2_PRESETS),
#                 CurlOpt.FRESH_CONNECT: 1,
#                 CurlOpt.FORBID_REUSE: 1,
#             }

#             proxies = get_proxy(currency=params.task__parsing_price_variables_currency)

#             # Step 2: Make the request
#             # Build dynamic extra fingerprints for this attempt
#             sig_count = random.randint(2, len(SIG_ALG_POOL))
#             sigs = random.sample(SIG_ALG_POOL, sig_count)
#             random.shuffle(sigs)
#             fp_kwargs = dict(
#                 tls_grease=True,
#                 tls_permute_extensions=True,
#                 tls_cert_compression="brotli",
#                 tls_signature_algorithms=sigs,
#             )

#             if HAS_session_ticket_disable:
#                 # Recommended for better privacy
#                 fp_kwargs["tls_session_ticket_disable"] = True

#             if HAS_disable_sigs:
#                 # Choose 1-2 algs to drop so the *set* changes → JA4 changes
#                 drop_cnt = random.randint(1, min(2, len(sigs)-1))
#                 sigs_to_disable = random.sample(sigs, drop_cnt)
#                 fp_kwargs["tls_disable_sigs"] = sigs_to_disable

#             if HAS_akamai_fp:
#                 # Use one of the AKAMAI_PRESETS for the fingerprint
#                 fp_kwargs["akamai"] = random.choice(AKAMAI_PRESETS)

#             extra_fp = ExtraFingerprints(**fp_kwargs)

#             hdr_items = list(config["headers"].items())
#             random.shuffle(hdr_items)
#             headers = {_rand_case(k): v for k, v in hdr_items}

#             time.sleep(random.uniform(0.3, 0.8))

#             response = requests.post(
#                 config["url"],
#                 headers=headers,
#                 json=config["payload"],
#                 impersonate=config["impersonate"],   # rotate browser version
#                 extra_fp=extra_fp,                  # randomised TLS details
#                 proxies=proxies,
#                 verify=False,
#                 curl_options=CURL_OPTS,       # low-level tweaks
#             )

#             # Step 3: Process response
#             if response.status_code == 200:
#                 data = response.json()
#                 attempt_data = {
#                     "success": True,
#                     "data": data,
#                     "retries": attempt + 1,
#                 }
#                 attempt_success = True
#                 if response.status_code == 429:
#                     if params.task__parsing_price_variables_currency == "USD" or params.task__parsing_price_variables_currency == "GBP":
#                         wait = 6
#                     else:
#                         wait = int(response.headers.get("Retry-After", "2"))
#                     time.sleep(wait)
#                     continue

#                 # Force a "continue" by raising an exception that we'll catch
#                 raise Exception(f"Non-200 status code: {response.status_code}")

#         except json.JSONDecodeError as e:
#             last_error = f"JSON decode error: {str(e)}"
#             log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#                 log_message=f"Failed to parse JSON response: {str(e)}", log_level="ERROR")

#         except Exception as e:
#             last_error = str(e)


#         finally:
#             # Update overall success status from this attempt
#             if attempt_success:
#                 success = True
#                 response_data = attempt_data
#                 break  # Exit the retry loop on success

#             # Don't do anything else in finally - just proceed to next attempt

#     # After all attempts or when successful
#     if success:
#         return response_data
#     else:
#         log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#             log_message=f"Failed after {max_retries} attempts. Last error: {last_error}", log_level="ERROR")
#         return {
#             "success": False,
#             "error": last_error or "Unknown error",
#             "retries": max_retries
#         }


# def _rand_case(s):     # keep your helper handy
#     return "".join(c.upper() if random.random() < .5 else c for c in s)
# from ...app_config import get_config
# from curl_cffi import requests
# import json
# import time
# import random
# from .http_proxy import get_proxy
# from ...logging import log
# from ...common.common_get_proxy_ip import get_proxy_ip
# from curl_cffi.const import CurlOpt
# from curl_cffi.requests import ExtraFingerprints


# SIG_ALG_POOL = [
#     "ecdsa_secp256r1_sha256", "ecdsa_secp384r1_sha384",
#     "rsa_pss_rsae_sha256",    "rsa_pss_rsae_sha512",
#     "rsa_pkcs1_sha256",       "rsa_pkcs1_sha512",
# ]

# # Capability checks
# FP_FIELDS = ExtraFingerprints.__dataclass_fields__.keys()
# HAS_disable_sigs = "tls_disable_sigs" in FP_FIELDS
# HAS_akamai_fp = "akamai" in FP_FIELDS
# HAS_session_ticket_disable = "tls_session_ticket_disable" in FP_FIELDS

# H2_PRESETS = [
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=1000,MAX_HEADER_LIST_SIZE=262144",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=131072,"
#     "MAX_CONCURRENT_STREAMS=100,MAX_HEADER_LIST_SIZE=32768",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=200,MAX_HEADER_LIST_SIZE=262144",
# ]


# AKAMAI_PRESETS = [
#     "|10485760|0|m,s,p,a",
#     "|15663105|0|m,a,s,p",
#     "|11534336|0|m,p,a,s",
#     "|14680064|0|s,m,p,a",
# ]


# def make_request(params, max_retries=25) -> dict:
#     """
#     Make a request to the API with retry logic and proxy support.

#     Args:
#         params: Request parameters
#         max_retries: Maximum number of retry attempts

#     Returns:
#         dict: Response data with success indicator. Always includes 'success' key.
#               If successful: {'success': True, 'data': response_data, ...}
#               If failed: {'success': False, 'error': error_message, 'retries': max_retries}
#     """
#     last_error = None
#     success = False
#     response_data = None

#     for attempt in range(max_retries):
#         # Wait before retrying (skip waiting before first attempt)
#         if attempt > 0:
#             # First delay is 5 seconds, then increment by 5 seconds for each subsequent retry
#             # wait_seconds = 5 * attempt
#             # time.sleep(wait_seconds)
#             pass

#         # Reset state for this attempt
#         attempt_success = False
#         attempt_data = None

#         try:
#             # Step 1: Get config and proxy
#             config = get_config(params)

#             CURL_OPTS = {
#                 # — Kill connection reuse so every retry is a fresh fingerprint —
#                 # ← add this
#                 CurlOpt.HTTP2_SETTINGS: random.choice(H2_PRESETS),
#                 CurlOpt.FRESH_CONNECT: 1,
#                 CurlOpt.FORBID_REUSE: 1,
#             }

#             proxies = get_proxy(currency=params.task__parsing_price_variables_currency)

#             # Step 2: Make the request
#             # Build dynamic extra fingerprints for this attempt
#             sig_count = random.randint(2, len(SIG_ALG_POOL))
#             sigs = random.sample(SIG_ALG_POOL, sig_count)
#             random.shuffle(sigs)
#             fp_kwargs = dict(
#                 tls_grease=True,
#                 tls_permute_extensions=True,
#                 tls_cert_compression="brotli",
#                 tls_signature_algorithms=sigs,
#             )

#             if HAS_session_ticket_disable:
#                 # Recommended for better privacy
#                 fp_kwargs["tls_session_ticket_disable"] = True

#             if HAS_disable_sigs:
#                 # Choose 1-2 algs to drop so the *set* changes → JA4 changes
#                 drop_cnt = random.randint(1, min(2, len(sigs)-1))
#                 sigs_to_disable = random.sample(sigs, drop_cnt)
#                 fp_kwargs["tls_disable_sigs"] = sigs_to_disable

#             if HAS_akamai_fp:
#                 # Use one of the AKAMAI_PRESETS for the fingerprint
#                 fp_kwargs["akamai"] = random.choice(AKAMAI_PRESETS)

#             extra_fp = ExtraFingerprints(**fp_kwargs)

#             hdr_items = list(config["headers"].items())
#             random.shuffle(hdr_items)
#             headers = {_rand_case(k): v for k, v in hdr_items}

#             time.sleep(random.uniform(0.3, 0.8))

#             response = requests.post(
#                 config["url"],
#                 headers=headers,
#                 json=config["payload"],
#                 impersonate=config["impersonate"],   # rotate browser version
#                 extra_fp=extra_fp,                  # randomised TLS details
#                 proxies=proxies,
#                 verify=False,
#                 curl_options=CURL_OPTS,       # low-level tweaks
#             )

#             # Step 3: Process response
#             if response.status_code == 200:
#                 data = response.json()
#                 attempt_data = {
#                     "success": True,
#                     "data": data,
#                     "retries": attempt + 1,
#                 }
#                 attempt_success = True
#                 if response.status_code == 429:
#                     if params.task__parsing_price_variables_currency == "USD" or params.task__parsing_price_variables_currency == "GBP":
#                         wait = 6
#                     else:
#                         wait = int(response.headers.get("Retry-After", "2"))
#                     time.sleep(wait)
#                     continue

#                 # Force a "continue" by raising an exception that we'll catch
#                 raise Exception(f"Non-200 status code: {response.status_code}")

#         except json.JSONDecodeError as e:
#             last_error = f"JSON decode error: {str(e)}"
#             log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#                 log_message=f"Failed to parse JSON response: {str(e)}", log_level="ERROR")

#         except Exception as e:
#             last_error = str(e)


#         finally:
#             # Update overall success status from this attempt
#             if attempt_success:
#                 success = True
#                 response_data = attempt_data
#                 break  # Exit the retry loop on success

#             # Don't do anything else in finally - just proceed to next attempt

#     # After all attempts or when successful
#     if success:
#         return response_data
#     else:
#         log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#             log_message=f"Failed after {max_retries} attempts. Last error: {last_error}", log_level="ERROR")
#         return {
#             "success": False,
#             "error": last_error or "Unknown error",
#             "retries": max_retries
#         }


# def _rand_case(s):     # keep your helper handy
#     return "".join(c.upper() if random.random() < .5 else c for c in s)
# from ...app_config import get_config
# from curl_cffi import requests
# import json
# import time
# import random
# from .http_proxy import get_proxy
# from ...logging import log
# from ...common.common_get_proxy_ip import get_proxy_ip
# from curl_cffi.const import CurlOpt
# from curl_cffi.requests import ExtraFingerprints


# SIG_ALG_POOL = [
#     "ecdsa_secp256r1_sha256", "ecdsa_secp384r1_sha384",
#     "rsa_pss_rsae_sha256",    "rsa_pss_rsae_sha512",
#     "rsa_pkcs1_sha256",       "rsa_pkcs1_sha512",
# ]

# # Capability checks
# FP_FIELDS = ExtraFingerprints.__dataclass_fields__.keys()
# HAS_disable_sigs = "tls_disable_sigs" in FP_FIELDS
# HAS_akamai_fp = "akamai" in FP_FIELDS
# HAS_session_ticket_disable = "tls_session_ticket_disable" in FP_FIELDS

# H2_PRESETS = [
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=1000,MAX_HEADER_LIST_SIZE=262144",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=131072,"
#     "MAX_CONCURRENT_STREAMS=100,MAX_HEADER_LIST_SIZE=32768",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=200,MAX_HEADER_LIST_SIZE=262144",
# ]


# AKAMAI_PRESETS = [
#     "|10485760|0|m,s,p,a",
#     "|15663105|0|m,a,s,p",
#     "|11534336|0|m,p,a,s",
#     "|14680064|0|s,m,p,a",
# ]


# def make_request(params, max_retries=25) -> dict:
#     """
#     Make a request to the API with retry logic and proxy support.

#     Args:
#         params: Request parameters
#         max_retries: Maximum number of retry attempts

#     Returns:
#         dict: Response data with success indicator. Always includes 'success' key.
#               If successful: {'success': True, 'data': response_data, ...}
#               If failed: {'success': False, 'error': error_message, 'retries': max_retries}
#     """
#     last_error = None
#     success = False
#     response_data = None

#     for attempt in range(max_retries):
#         # Wait before retrying (skip waiting before first attempt)
#         if attempt > 0:
#             # First delay is 5 seconds, then increment by 5 seconds for each subsequent retry
#             # wait_seconds = 5 * attempt
#             # time.sleep(wait_seconds)
#             pass

#         # Reset state for this attempt
#         attempt_success = False
#         attempt_data = None

#         try:
#             # Step 1: Get config and proxy
#             config = get_config(params)

#             CURL_OPTS = {
#                 # — Kill connection reuse so every retry is a fresh fingerprint —
#                 # ← add this
#                 CurlOpt.HTTP2_SETTINGS: random.choice(H2_PRESETS),
#                 CurlOpt.FRESH_CONNECT: 1,
#                 CurlOpt.FORBID_REUSE: 1,
#             }

#             proxies = get_proxy(currency=params.task__parsing_price_variables_currency)

#             # Step 2: Make the request
#             # Build dynamic extra fingerprints for this attempt
#             sig_count = random.randint(2, len(SIG_ALG_POOL))
#             sigs = random.sample(SIG_ALG_POOL, sig_count)
#             random.shuffle(sigs)
#             fp_kwargs = dict(
#                 tls_grease=True,
#                 tls_permute_extensions=True,
#                 tls_cert_compression="brotli",
#                 tls_signature_algorithms=sigs,
#             )

#             if HAS_session_ticket_disable:
#                 # Recommended for better privacy
#                 fp_kwargs["tls_session_ticket_disable"] = True

#             if HAS_disable_sigs:
#                 # Choose 1-2 algs to drop so the *set* changes → JA4 changes
#                 drop_cnt = random.randint(1, min(2, len(sigs)-1))
#                 sigs_to_disable = random.sample(sigs, drop_cnt)
#                 fp_kwargs["tls_disable_sigs"] = sigs_to_disable

#             if HAS_akamai_fp:
#                 # Use one of the AKAMAI_PRESETS for the fingerprint
#                 fp_kwargs["akamai"] = random.choice(AKAMAI_PRESETS)

#             extra_fp = ExtraFingerprints(**fp_kwargs)

#             hdr_items = list(config["headers"].items())
#             random.shuffle(hdr_items)
#             headers = {_rand_case(k): v for k, v in hdr_items}

#             time.sleep(random.uniform(0.3, 0.8))

#             response = requests.post(
#                 config["url"],
#                 headers=headers,
#                 json=config["payload"],
#                 impersonate=config["impersonate"],   # rotate browser version
#                 extra_fp=extra_fp,                  # randomised TLS details
#                 proxies=proxies,
#                 verify=False,
#                 curl_options=CURL_OPTS,       # low-level tweaks
#             )

#             # Step 3: Process response
#             if response.status_code == 200:
#                 data = response.json()
#                 attempt_data = {
#                     "success": True,
#                     "data": data,
#                     "retries": attempt + 1,
#                 }
#                 attempt_success = True
#                 if response.status_code == 429:
#                     if params.task__parsing_price_variables_currency == "USD" or params.task__parsing_price_variables_currency == "GBP":
#                         wait = 6
#                     else:
#                         wait = int(response.headers.get("Retry-After", "2"))
#                     time.sleep(wait)
#                     continue

#                 # Force a "continue" by raising an exception that we'll catch
#                 raise Exception(f"Non-200 status code: {response.status_code}")

#         except json.JSONDecodeError as e:
#             last_error = f"JSON decode error: {str(e)}"
#             log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#                 log_message=f"Failed to parse JSON response: {str(e)}", log_level="ERROR")

#         except Exception as e:
#             last_error = str(e)


#         finally:
#             # Update overall success status from this attempt
#             if attempt_success:
#                 success = True
#                 response_data = attempt_data
#                 break  # Exit the retry loop on success

#             # Don't do anything else in finally - just proceed to next attempt

#     # After all attempts or when successful
#     if success:
#         return response_data
#     else:
#         log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#             log_message=f"Failed after {max_retries} attempts. Last error: {last_error}", log_level="ERROR")
#         return {
#             "success": False,
#             "error": last_error or "Unknown error",
#             "retries": max_retries
#         }


# def _rand_case(s):     # keep your helper handy
#     return "".join(c.upper() if random.random() < .5 else c for c in s)
# from ...app_config import get_config
# from curl_cffi import requests
# import json
# import time
# import random
# from .http_proxy import get_proxy
# from ...logging import log
# from ...common.common_get_proxy_ip import get_proxy_ip
# from curl_cffi.const import CurlOpt
# from curl_cffi.requests import ExtraFingerprints


# SIG_ALG_POOL = [
#     "ecdsa_secp256r1_sha256", "ecdsa_secp384r1_sha384",
#     "rsa_pss_rsae_sha256",    "rsa_pss_rsae_sha512",
#     "rsa_pkcs1_sha256",       "rsa_pkcs1_sha512",
# ]

# # Capability checks
# FP_FIELDS = ExtraFingerprints.__dataclass_fields__.keys()
# HAS_disable_sigs = "tls_disable_sigs" in FP_FIELDS
# HAS_akamai_fp = "akamai" in FP_FIELDS
# HAS_session_ticket_disable = "tls_session_ticket_disable" in FP_FIELDS

# H2_PRESETS = [
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=1000,MAX_HEADER_LIST_SIZE=262144",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=131072,"
#     "MAX_CONCURRENT_STREAMS=100,MAX_HEADER_LIST_SIZE=32768",
#     "HEADER_TABLE_SIZE=65536,INITIAL_WINDOW_SIZE=6291456,"
#     "MAX_CONCURRENT_STREAMS=200,MAX_HEADER_LIST_SIZE=262144",
# ]


# AKAMAI_PRESETS = [
#     "|10485760|0|m,s,p,a",
#     "|15663105|0|m,a,s,p",
#     "|11534336|0|m,p,a,s",
#     "|14680064|0|s,m,p,a",
# ]


# def make_request(params, max_retries=25) -> dict:
#     """
#     Make a request to the API with retry logic and proxy support.

#     Args:
#         params: Request parameters
#         max_retries: Maximum number of retry attempts

#     Returns:
#         dict: Response data with success indicator. Always includes 'success' key.
#               If successful: {'success': True, 'data': response_data, ...}
#               If failed: {'success': False, 'error': error_message, 'retries': max_retries}
#     """
#     last_error = None
#     success = False
#     response_data = None

#     for attempt in range(max_retries):
#         # Wait before retrying (skip waiting before first attempt)
#         if attempt > 0:
#             # First delay is 5 seconds, then increment by 5 seconds for each subsequent retry
#             # wait_seconds = 5 * attempt
#             # time.sleep(wait_seconds)
#             pass

#         # Reset state for this attempt
#         attempt_success = False
#         attempt_data = None

#         try:
#             # Step 1: Get config and proxy
#             config = get_config(params)

#             CURL_OPTS = {
#                 # — Kill connection reuse so every retry is a fresh fingerprint —
#                 # ← add this
#                 CurlOpt.HTTP2_SETTINGS: random.choice(H2_PRESETS),
#                 CurlOpt.FRESH_CONNECT: 1,
#                 CurlOpt.FORBID_REUSE: 1,
#             }

#             proxies = get_proxy(currency=params.task__parsing_price_variables_currency)

#             # Step 2: Make the request
#             # Build dynamic extra fingerprints for this attempt
#             sig_count = random.randint(2, len(SIG_ALG_POOL))
#             sigs = random.sample(SIG_ALG_POOL, sig_count)
#             random.shuffle(sigs)
#             fp_kwargs = dict(
#                 tls_grease=True,
#                 tls_permute_extensions=True,
#                 tls_cert_compression="brotli",
#                 tls_signature_algorithms=sigs,
#             )

#             if HAS_session_ticket_disable:
#                 # Recommended for better privacy
#                 fp_kwargs["tls_session_ticket_disable"] = True

#             if HAS_disable_sigs:
#                 # Choose 1-2 algs to drop so the *set* changes → JA4 changes
#                 drop_cnt = random.randint(1, min(2, len(sigs)-1))
#                 sigs_to_disable = random.sample(sigs, drop_cnt)
#                 fp_kwargs["tls_disable_sigs"] = sigs_to_disable

#             if HAS_akamai_fp:
#                 # Use one of the AKAMAI_PRESETS for the fingerprint
#                 fp_kwargs["akamai"] = random.choice(AKAMAI_PRESETS)

#             extra_fp = ExtraFingerprints(**fp_kwargs)

#             hdr_items = list(config["headers"].items())
#             random.shuffle(hdr_items)
#             headers = {_rand_case(k): v for k, v in hdr_items}

#             time.sleep(random.uniform(0.3, 0.8))

#             response = requests.post(
#                 config["url"],
#                 headers=headers,
#                 json=config["payload"],
#                 impersonate=config["impersonate"],   # rotate browser version
#                 extra_fp=extra_fp,                  # randomised TLS details
#                 proxies=proxies,
#                 verify=False,
#                 curl_options=CURL_OPTS,       # low-level tweaks
#             )

#             # Step 3: Process response
#             if response.status_code == 200:
#                 data = response.json()
#                 attempt_data = {
#                     "success": True,
#                     "data": data,
#                     "retries": attempt + 1,
#                 }
#                 attempt_success = True
#                 if response.status_code == 429:
#                     if params.task__parsing_price_variables_currency == "USD" or params.task__parsing_price_variables_currency == "GBP":
#                         wait = 6
#                     else:
#                         wait = int(response.headers.get("Retry-After", "2"))
#                     time.sleep(wait)
#                     continue

#                 # Force a "continue" by raising an exception that we'll catch
#                 raise Exception(f"Non-200 status code: {response.status_code}")

#         except json.JSONDecodeError as e:
#             last_error = f"JSON decode error: {str(e)}"
#             log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#                 log_message=f"Failed to parse JSON response: {str(e)}", log_level="ERROR")

#         except Exception as e:
#             last_error = str(e)


#         finally:
#             # Update overall success status from this attempt
#             if attempt_success:
#                 success = True
#                 response_data = attempt_data
#                 break  # Exit the retry loop on success

#             # Don't do anything else in finally - just proceed to next attempt

#     # After all attempts or when successful
#     if success:
#         return response_data
#     else:
#         log(individual_id=params.task_id, log_path="app/utils/http/http_request.py | make_request",
#             log_message=f"Failed after {max_retries} attempts. Last error: {last_error}", log_level="ERROR")
#         return {
#             "success": False,
#             "error": last_error or "Unknown error",
#             "retries": max_retries
#         }


# def _rand_case(s):     # keep your helper handy
#     return "".join(c.upper() if random.random() < .5 else c for c in s)
