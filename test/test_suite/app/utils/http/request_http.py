from __future__ import annotations

import asyncio
import secrets
import time
from typing import Any
from urllib.parse import urlparse
from curl_cffi import requests
from curl_cffi.const import CurlOpt
from curl_cffi.requests import ExtraFingerprints, Response
from ...types import RequestParameters, SyncResponse

PATCH_POOL = [
    "7103.32",
    "7103.48",
    "7103.49",
    "7103.93",
    "7103.94",
    "7103.113",
    "7103.114",
]

patch = secrets.choice(PATCH_POOL)
PROFILES: dict[str, dict[str, Any]] = {
    "chrome136": {
        "sig_algs": [
            "ecdsa_secp256r1_sha256",
            "ecdsa_secp384r1_sha384",
            "rsa_pss_rsae_sha256",
            "rsa_pss_rsae_sha384",
            "rsa_pss_rsae_sha512",
            "rsa_pkcs1_sha256",
            "rsa_pkcs1_sha384",
            "rsa_pkcs1_sha1",
        ],
        "headers": {
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            "accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7"
            ),
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br, zstd",
            "sec-ch-ua": ('"Chromium";v="136", "Google Chrome";v="136", "Not A;Brand";v="24"'),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        },
        "h2_range": {
            "HEADER_TABLE_SIZE": [16384, 65536],
            "INITIAL_WINDOW_SIZE": [6291456],
            "MAX_CONCURRENT_STREAMS": [100, 256, 1000],
            "MAX_HEADER_LIST_SIZE": [262144, 524288],
        },
    },
}

PROFILE_NAMES: list[str] = list(PROFILES.keys())


class Request:
    def __init__(self, params: RequestParameters) -> None:
        self.params = params
        self.impersonation = secrets.choice(PROFILE_NAMES)
        self.profile = PROFILES[self.impersonation]
        self.randomized_headers: dict[str, str] = {}
        self.curl_opts: dict[int, Any] = {}

    # ---------- timing utilities ----------
    @staticmethod
    def _micro_pause() -> None:
        time.sleep(0.1)

    @staticmethod
    def _backoff_sync(attempt: int) -> None:
        back = max(1, min(30, 2**attempt))
        time.sleep(back * 1.0)

    @staticmethod
    async def _backoff_async(attempt: int) -> None:
        back = max(1, min(30, 2**attempt))
        await asyncio.sleep(back * 1.0)

    @staticmethod
    def _short_jitter() -> None:
        time.sleep(0.3)

    @staticmethod
    async def _short_jitter_async() -> None:
        await asyncio.sleep(0.3)

    # ---------- fingerprint + headers -------
    def _build_fp_and_headers(self) -> ExtraFingerprints:
        reuse = secrets.randbelow(100) < 75
        alpn_on = 1
        if not reuse and secrets.randbelow(100) < 10:
            alpn_on = 0  # HTTP/1.1 trial

        self.curl_opts = {
            CurlOpt.FRESH_CONNECT: 1,
            CurlOpt.FORBID_REUSE: 1,
            CurlOpt.SSL_SESSIONID_CACHE: int(reuse),
            CurlOpt.SSL_ENABLE_TICKET: int(reuse),
            CurlOpt.SSL_ENABLE_ALPN: alpn_on,
            CurlOpt.CONNECTTIMEOUT_MS: 8000,
            CurlOpt.LOW_SPEED_TIME: 15,
        }

        sigs = self.profile["sig_algs"].copy()
        sigs = sigs[:4] + secrets.SystemRandom().sample(sigs[4:], len(sigs) - 4)

        # Only add tls_cert_compression when we actually want Brotli
        fp_kwargs: dict[str, Any] = dict(
            tls_grease=True,
            tls_permute_extensions=False,
            tls_signature_algorithms=sigs,
        )
        # Chrome / Edge sometimes advertise Brotli; Safari never does
        if not self.impersonation.startswith("safari") and secrets.randbelow(100) < 50:
            fp_kwargs["tls_cert_compression"] = "brotli"

        fp = ExtraFingerprints(**fp_kwargs)

        rng = self.profile["h2_range"]
        http2_settings = (
            f"HEADER_TABLE_SIZE={secrets.choice(rng['HEADER_TABLE_SIZE'])},"
            f"INITIAL_WINDOW_SIZE={secrets.choice(rng['INITIAL_WINDOW_SIZE'])},"
            f"MAX_CONCURRENT_STREAMS={secrets.choice(rng['MAX_CONCURRENT_STREAMS'])},"
            f"MAX_HEADER_LIST_SIZE={secrets.choice(rng['MAX_HEADER_LIST_SIZE'])}"
        )
        fp.http2_settings = http2_settings # type: ignore[attr-defined]

        hdrs: dict[str, str] = self.profile["headers"].copy()
        if alpn_on == 0:
            hdrs["host"] = urlparse(self.params["url"]).netloc
        request_headers = self.params.get("request_headers")
        if request_headers:
            hdrs.update({k.lower(): v for k, v in request_headers.items()})

        stable = [
            "host",
            "user-agent",
            "accept",
            "accept-encoding",
            "accept-language",
            "sec-ch-ua",
            "sec-ch-ua-mobile",
            "sec-ch-ua-platform",
        ]
        tail = [h for h in hdrs if h not in stable]
        secrets.SystemRandom().shuffle(tail)
        order = [h for h in stable if h in hdrs] + tail

        self.randomized_headers = {k: hdrs[k] for k in order}
        fp.header_order = order # type: ignore[attr-defined]
        self._micro_pause()
        return fp

    # ---------- helper for normal GET/POST ---
    def _do_sync(
        self,
        method: str,
        *,
        cookies: dict[str, str] | None = None,
        data: Any = None,
        params: Any = None,
    ) -> SyncResponse:
        proxy = {}
        proxy_url = self.params.get("request_proxy" , {})
        if proxy_url:
            proxy = {"https": proxy_url, "http": proxy_url}
        fp = self._build_fp_and_headers()
        response: Response = getattr(requests, method)(
            self.params["url"],
            headers=self.randomized_headers,
            data=data,
            params=params,
            impersonate=self.impersonation,
            proxies=proxy,
            extra_fp=fp,
            curl_options=self.curl_opts,
            verify=True,
            allow_redirects=True,
            timeout=25,
            cookies=cookies or {},
        )
        return SyncResponse(response=response, fingerprint=fp, request_headers=self.randomized_headers)


    # ---------- public wrappers --------------
    def curl_request_api_post(self) -> SyncResponse:
        return self._do_sync(
            method="post", cookies=self.params.get("request_cookies"), data=self.params.get("request_body"), params=self.params.get("request_params")
        )

    def curl_request_api_get(self) -> SyncResponse:
        return self._do_sync("get", cookies=self.params.get("request_cookies"), params=self.params.get("request_params"), data=self.params.get("request_body"))

    def curl_request_html_get(self) -> SyncResponse:
        return self._do_sync("get", cookies=self.params.get("request_cookies"), params=self.params.get("request_params"), data=self.params.get("request_body"))

    # ---------- async POST -------------------
    async def curl_request_api_post_async(self) -> Response:
        from curl_cffi.requests import AsyncSession

        fp = self._build_fp_and_headers()
        proxy = {}
        proxy_url = self.params.get("request_proxy" , {})
        if proxy_url:
            proxy = {"https": proxy_url, "http": proxy_url}
        async with AsyncSession(
            impersonate=self.impersonation,  # type: ignore[arg-type]
            proxies=proxy,  # type: ignore[arg-type]
            verify=True,
            timeout=25,
        ) as session:
            resp = await session.post(
                self.params["url"],
                headers=self.randomized_headers,
                data=self.params.payload,  # type: ignore[arg-type]
                extra_fp=fp,
                allow_redirects=True,
                cookies=self.params.get("request_cookies"),
            )

        return resp
