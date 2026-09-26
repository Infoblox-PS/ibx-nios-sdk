# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_tls.py
"""TLS/connect-error wrapping behavior for HttpClient."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import NiosConnectionError
from tests.conftest import make_http_client


async def test_tls_error_wrapped_with_helpful_message() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED] self signed certificate")

    client = make_http_client(handler)
    try:
        with pytest.raises(NiosConnectionError) as exc_info:
            await client.request("GET", "/grid")
        msg = exc_info.value.message
        assert "TLS verification failed" in msg
        assert "verify=False" in msg
        assert "ca_bundle" in msg
    finally:
        await client.aclose()


async def test_non_tls_connect_error_also_wrapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Name or service not known")

    client = make_http_client(handler)
    try:
        with pytest.raises(NiosConnectionError):
            await client.request("GET", "/grid")
    finally:
        await client.aclose()
