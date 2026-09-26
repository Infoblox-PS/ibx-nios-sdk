# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_session_auth.py
"""Session-cookie authentication: lazy login, cookie reuse, logout on close."""

from __future__ import annotations

import base64

import httpx

from tests.conftest import json_response, make_http_client


async def test_lazy_login_on_first_request() -> None:
    calls: list[tuple[str, str, bytes]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append((request.method, request.url.path, request.url.query))
        if request.headers.get("Authorization", "").startswith("Basic "):
            auth = request.headers.get("Authorization", "")
            assert auth.startswith("Basic "), "login should send HTTP Basic credentials"
            decoded = base64.b64decode(auth.removeprefix("Basic ")).decode()
            assert decoded == "admin:infoblox"
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=session-token-123; Path=/"},
            )
        # Subsequent calls must carry the cookie, not basic auth.
        assert "Authorization" not in request.headers or not request.headers[
            "Authorization"
        ].startswith("Basic ")
        assert "ibapauth=session-token-123" in request.headers.get("Cookie", "")
        return json_response({"_ref": "grid/b25lLmNsdXN0ZXIkMA:Infoblox"})

    client = make_http_client(handler)
    try:
        await client.request("GET", "/grid")
        # Login call was made exactly once + the actual /grid call = 2 total.
        assert len(calls) == 2
        assert calls[0][1].endswith("/") and b"_schema=1" in calls[0][2]

        # Second request should reuse the cookie, not re-login.
        await client.request("GET", "/grid")
        assert len(calls) == 3
        assert calls[2][1].endswith("/grid")
    finally:
        await client.aclose()


async def test_logout_on_close() -> None:
    logout_called = False

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal logout_called
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        if request.url.path.endswith("/logout"):
            logout_called = True
            return httpx.Response(200, json={})
        return json_response({})

    client = make_http_client(handler)
    await client.request("GET", "/grid")
    await client.aclose()
    assert logout_called
