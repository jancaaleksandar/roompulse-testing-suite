# from curl_cffi import requests
# import time
# import random
# from typing import Dict, Any, Optional, cast
# from curl_cffi.const import CurlOpt
# from curl_cffi.requests import ExtraFingerprints
# from ..types import RequestParameters, SyncResponse

# IMPERSONATIONS = [    
# 'chrome116',
# 'chrome120',
# 'chrome123',
# 'chrome124',
# 'safari17_0',
# ]


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


# def request_expedia_live(params: RequestParameters) -> SyncResponse:
#     """
#     Make a request to the API with retry logic and proxy support.
#     """
#     CURL_OPTS = {
#         CurlOpt.HTTP2_SETTINGS: random.choice(H2_PRESETS),
#         CurlOpt.FRESH_CONNECT: 1,
#         CurlOpt.FORBID_REUSE: 1,
#     }

#     # Build dynamic extra fingerprints for this attempt
#     sig_count = random.randint(2, len(SIG_ALG_POOL))
#     sigs = random.sample(SIG_ALG_POOL, sig_count)
#     random.shuffle(sigs)
    
#     # Build fingerprint kwargs with proper types
#     fp_kwargs: Dict[str, Any] = {
#         "tls_grease": True,
#         "tls_permute_extensions": True,
#         "tls_cert_compression": "brotli",
#         "tls_signature_algorithms": sigs,
#     }

#     if HAS_session_ticket_disable:
#         fp_kwargs["tls_session_ticket_disable"] = True

#     if HAS_disable_sigs and len(sigs) > 1:
#         drop_cnt = random.randint(1, min(2, len(sigs)-1))
#         sigs_to_disable = random.sample(sigs, drop_cnt)
#         fp_kwargs["tls_disable_sigs"] = sigs_to_disable

#     if HAS_akamai_fp:
#         fp_kwargs["akamai"] = random.choice(AKAMAI_PRESETS)

#     extra_fp = ExtraFingerprints(**fp_kwargs)

#     # Prepare headers
#     hdr_items = list(params['request_headers'].items()) if params['request_headers'] else []
#     random.shuffle(hdr_items)
#     headers = {_rand_case(k): v for k, v in hdr_items}

#     # Prepare proxy in the format curl_cffi expects
#     proxy_dict: Optional[Dict[str, str]] = None
#     if params['request_proxy'] and params['request_proxy'].get('proxy_url'):
#         proxy_url = params['request_proxy']['proxy_url']
#         proxy_dict = {
#             'http': proxy_url,
#             'https': proxy_url
#         }

#     time.sleep(random.uniform(0.3, 0.8))

#     # Make the request with proper error handling
#     try:
#         response = requests.post(
#             # params['url'],
#             'https://www.httpbin.org/anything',
#             headers=headers,
#             data=params['request_body'],
#             impersonate=cast(Any, random.choice(IMPERSONATIONS)),  # type: ignore
#             extra_fp=extra_fp,
#             proxies=cast(Any, proxy_dict),  # type: ignore
#             verify=False,
#             curl_options=CURL_OPTS,
#             timeout=30,  # Add timeout to prevent hanging
#         )

#         return SyncResponse(
#             response=response,
#             fingerprint=extra_fp,
#             request_headers=headers
#         )
        
#     except Exception as e:
#         # Re-raise with more context
#         raise Exception(f"Request failed: {str(e)}")


# def _rand_case(s: str) -> str:
#     """Randomly change case of characters in a string."""
#     return "".join(c.upper() if random.random() < 0.5 else c for c in s)