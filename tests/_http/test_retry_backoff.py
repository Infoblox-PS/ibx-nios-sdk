# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_retry_backoff.py
"""Exponential backoff + Retry-After on 429, 502, 503, 504. No retry on 500."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import RateLimitError, ServerError
from tests.conftest import json_response, make_http_client


async def test_retry_on_503_then_success(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", fake_sleep)

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        if calls < 3:
            return json_response({"Error": "busy"}, status_code=503)
        return json_response({"_ref": "grid/x:g"})

    client = make_http_client(handler)
    try:
        data = await client.request("GET", "/grid")
        assert data == {"_ref": "grid/x:g"}
        assert calls == 3
        assert len(sleeps) == 2
    finally:
        await client.aclose()


async def test_retry_after_header_respected(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", fake_sleep)

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        if calls == 1:
            return httpx.Response(
                429,
                json={"Error": "rate"},
                headers={"Retry-After": "2", "Content-Type": "application/json"},
            )
        return json_response({"_ref": "grid/x:g"})

    client = make_http_client(handler)
    try:
        await client.request("GET", "/grid")
        assert sleeps == [2.0]
    finally:
        await client.aclose()


async def test_500_not_retried() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        return json_response({"Error": "nope"}, status_code=500)

    client = make_http_client(handler, max_retries=3)
    try:
        with pytest.raises(ServerError):
            await client.request("GET", "/grid")
        assert calls == 1
    finally:
        await client.aclose()


async def test_retries_exhausted_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_sleep(delay: float) -> None:
        return None

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", fake_sleep)

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        return httpx.Response(429, json={"Error": "rate"}, headers={"Retry-After": "0"})

    client = make_http_client(handler, max_retries=2)
    try:
        with pytest.raises(RateLimitError):
            await client.request("GET", "/grid")
    finally:
        await client.aclose()
