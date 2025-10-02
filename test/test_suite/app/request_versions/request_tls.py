# from __future__ import annotations
# import asyncio, random, time
# from typing import Any, Dict, Optional
# import tls_client  # type: ignore
# from ..types import RequestParameters, SyncResponse

# # TLS-Client rotating fingerprints pool - using supported identifiers
# CLIENT_IDENTIFIERS = [
#     "chrome_103",
#     "chrome_104", 
#     "chrome_105",
#     "chrome_106",
#     "chrome_107",
#     "chrome_108",
#     "chrome_109",
#     "chrome_110",
#     "chrome_111",
#     "chrome_112",
#     "firefox_102",
#     "firefox_104",
#     "firefox_105",
#     "firefox_106",
#     "firefox_108",
#     "firefox_110",
#     "safari_15_3",
#     "safari_15_6_1",
#     "safari_16_0",
# ]

# # Response adapter to make tls_client.Response compatible with curl_cffi.Response
# class ResponseAdapter:  # type: ignore
#     def __init__(self, tls_response: Any) -> None:
#         self._tls_response = tls_response
    
#     def __getattr__(self, name: str) -> Any:
#         return getattr(self._tls_response, name)
    
#     @property 
#     def status_code(self) -> Any:
#         return self._tls_response.status_code
    
#     @property
#     def text(self) -> Any:
#         return self._tls_response.text
    
#     @property
#     def content(self) -> Any:
#         return self._tls_response.content
    
#     @property
#     def headers(self) -> Any:
#         return self._tls_response.headers
    
#     @property
#     def cookies(self) -> Any:
#         return self._tls_response.cookies

# # Fingerprint adapter to make it compatible with ExtraFingerprints
# class FingerprintAdapter:  # type: ignore
#     def __init__(self, client_id: str) -> None:
#         self.client_identifier = client_id
#         self.tls_grease = True
#         self.tls_permute_extensions = False

# class Request:
#     def __init__(self, params: RequestParameters) -> None:
#         self.params = params
#         self.client_identifier = random.choice(CLIENT_IDENTIFIERS)
#         self.session: Optional[tls_client.Session] = None
#         self.randomized_headers: Dict[str, str] = {}

#     # ---------- timing utilities ----------
#     @staticmethod
#     def _micro_pause() -> None:
#         time.sleep(random.choices(
#             [random.uniform(0.05, 0.2), random.uniform(0.5, 2.0)],
#             weights=[0.9, 0.1],
#         )[0])

#     @staticmethod
#     def _backoff_sync(attempt: int) -> None:
#         back = max(1, min(30, 2 ** attempt))
#         time.sleep(back * random.uniform(0.5, 1.5))

#     @staticmethod
#     async def _backoff_async(attempt: int) -> None:
#         back = max(1, min(30, 2 ** attempt))
#         await asyncio.sleep(back * random.uniform(0.5, 1.5))

#     @staticmethod
#     def _short_jitter() -> None:
#         time.sleep(random.uniform(0.1, 0.5))

#     @staticmethod
#     async def _short_jitter_async() -> None:
#         await asyncio.sleep(random.uniform(0.1, 0.5))

#     # ---------- session setup -------
#     def _setup_session(self) -> Any:  # type: ignore
#         """Create and configure a tls-client session with rotating fingerprint"""
#         if not self.session:
#             self.session = tls_client.Session(  # type: ignore
#                 client_identifier=self.client_identifier,  # type: ignore
#                 random_tls_extension_order=True
#             )
            
#             # Configure proxy if provided
#             request_proxy = self.params.get('request_proxy')
#             if request_proxy and request_proxy.get("proxy_url"):
#                 proxy_url = request_proxy["proxy_url"]
#                 self.session.proxies = {  # type: ignore
#                     "http": proxy_url,
#                     "https": proxy_url
#                 }
            
#             # Set base headers
#             base_headers = self._get_base_headers()
#             request_headers = self.params.get("request_headers")
#             if request_headers:
#                 base_headers.update({k.lower(): v for k, v in request_headers.items()})
            
#             self.randomized_headers = self._randomize_header_order(base_headers)
#             self.session.headers.update(self.randomized_headers)  # type: ignore
            
#             self._micro_pause()
        
#         return self.session

#     def _get_base_headers(self) -> Dict[str, str]:
#         """Get base headers based on client identifier"""
#         if "chrome" in self.client_identifier:
#             return {
#                 "accept": (
#                     "text/html,application/xhtml+xml,application/xml;q=0.9,"
#                     "image/avif,image/webp,image/apng,*/*;q=0.8,"
#                     "application/signed-exchange;v=b3;q=0.7"
#                 ),
#                 "accept-language": "en-US,en;q=0.9",
#                 "accept-encoding": "gzip, deflate, br, zstd",
#                 "sec-ch-ua-mobile": "?0",
#                 "sec-ch-ua-platform": '"Windows"',
#                 "sec-fetch-dest": "document",
#                 "sec-fetch-mode": "navigate",
#                 "sec-fetch-site": "none",
#                 "sec-fetch-user": "?1",
#                 "upgrade-insecure-requests": "1",
#             }
#         elif "firefox" in self.client_identifier:
#             return {
#                 "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#                 "accept-language": "en-US,en;q=0.5",
#                 "accept-encoding": "gzip, deflate, br",
#                 "upgrade-insecure-requests": "1",
#             }
#         elif "safari" in self.client_identifier:
#             return {
#                 "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#                 "accept-language": "en-us",
#                 "accept-encoding": "gzip, deflate, br",
#                 "upgrade-insecure-requests": "1",
#             }
#         else:  # opera or other
#             return {
#                 "accept": (
#                     "text/html,application/xhtml+xml,application/xml;q=0.9,"
#                     "image/avif,image/webp,image/apng,*/*;q=0.8,"
#                     "application/signed-exchange;v=b3;q=0.7"
#                 ),
#                 "accept-language": "en-US,en;q=0.9",
#                 "accept-encoding": "gzip, deflate, br, zstd",
#                 "upgrade-insecure-requests": "1",
#             }

#     def _randomize_header_order(self, headers: Dict[str, str]) -> Dict[str, str]:
#         """Randomize header order while keeping some stable ones first"""
#         stable = [
#             "host",
#             "user-agent", 
#             "accept",
#             "accept-encoding",
#             "accept-language",
#             "sec-ch-ua",
#             "sec-ch-ua-mobile",
#             "sec-ch-ua-platform",
#         ]
#         tail = [h for h in headers if h not in stable]
#         random.shuffle(tail)
#         order = [h for h in stable if h in headers] + tail
        
#         return {k: headers[k] for k in order}

#     # ---------- helper for normal GET/POST ---
#     def _do_sync(
#         self,
#         method: str,
#         *,
#         cookies: Optional[Dict[str, str]] = None,
#         data: Any = None,
#         params: Any = None,
#     ) -> SyncResponse:
#         max_retries = 3
#         for attempt in range(max_retries):
#             try:
#                 request_proxy = self.params.get('request_proxy')
#                 if not request_proxy or not request_proxy.get("proxy_url"):
#                     raise Exception("No proxy URL provided")
                    
#                 # Create a fresh session for each attempt to avoid connection reuse issues
#                 self.session = None
#                 session = self._setup_session()
                
#                 # Set cookies if provided
#                 if cookies:
#                     session.cookies.update(cookies)  # type: ignore
                
#                 # Prepare request arguments
#                 request_kwargs = {
#                     "allow_redirects": True,
#                 }
                
#                 # Add retry delay for subsequent attempts
#                 if attempt > 0:
#                     self._short_jitter()
                
#                 # Make the request
#                 if method.lower() == "get":
#                     response = session.get(  # type: ignore
#                         self.params["url"],
#                         params=params,
#                         **request_kwargs
#                     )
#                 elif method.lower() == "post":
#                     response = session.post(  # type: ignore
#                         self.params["url"],
#                         data=data,
#                         allow_redirects=True
#                     )
#                 else:
#                     raise ValueError(f"Unsupported method: {method}")
                
#                 # Wrap response and fingerprint for compatibility
#                 wrapped_response = ResponseAdapter(response)  # type: ignore
#                 wrapped_fingerprint = FingerprintAdapter(self.client_identifier)  # type: ignore
                
#                 return SyncResponse(  # type: ignore
#                     response=wrapped_response,  # type: ignore
#                     fingerprint=wrapped_fingerprint,  # type: ignore
#                     request_headers=self.randomized_headers
#                 )
                
#             except Exception as e:
#                 if attempt == max_retries - 1:  # Last attempt
#                     raise e
#                 # Wait before retry
#                 self._backoff_sync(attempt)
#                 continue
        
#         # This should never be reached due to the raise in the except block
#         raise Exception("All retry attempts failed")

#     # ---------- dedicated cookie fetch -------
#     def curl_request_cookie(self) -> Optional[str]:
#         """Fetch cookies from the URL - TODO: DELETE THIS FUNCTION"""
#         try:
#             request_proxy = self.params.get('request_proxy')
#             if not request_proxy or not request_proxy.get("proxy_url"):
#                 raise Exception("No proxy URL provided")
                
#             session = self._setup_session()
            
#             response = session.get(  # type: ignore
#                 self.params["url"],
#                 allow_redirects=True
#             )
            
#             if response.status_code == 200 and hasattr(response, 'cookies') and response.cookies:  # type: ignore
#                 return "; ".join(f"{name}={value}" for name, value in response.cookies.items())  # type: ignore
                
#         except Exception as e:
#             raise e

#     # ---------- public wrappers --------------
#     def curl_request_api_post(self) -> SyncResponse:
#         return self._do_sync(method="post", cookies=self.params.get("request_cookies"), data=self.params.get("request_body"))

#     def curl_request_api_get(self) -> SyncResponse:
#         return self._do_sync("get", cookies=self.params.get("request_cookies"), params=self.params.get("request_body"))

#     def curl_request_html_get(self) -> SyncResponse:
#         return self._do_sync("get", cookies=self.params.get("request_cookies"), params=self.params.get("request_body"))

#     # ---------- async POST -------------------
#     async def curl_request_api_post_async(self) -> Any:  # type: ignore
#         """Async POST request - Note: tls-client doesn't have native async support"""
#         # For now, we'll run the sync version in a thread pool
#         import concurrent.futures
        
#         loop = asyncio.get_event_loop()
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             future = loop.run_in_executor(
#                 executor, 
#                 self.curl_request_api_post
#             )
#             result = await future
#             return result["response"]  # type: ignore

#     def __del__(self):
#         """Clean up session when object is destroyed"""
#         if self.session:
#             try:
#                 self.session.close()
#             except:
#                 pass
