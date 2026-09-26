# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_auth_retry.py
"""401 auto-retry: one transparent re-login after 401, then propagate."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import AuthenticationError
from tests.conftest import json_response, make_http_client


async def test_401_triggers_single_relogin() -> None:
    login_count = 0
    grid_401_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal login_count, grid_401_count
        if request.headers.get("Authorization", "").startswith("Basic "):
            login_count += 1
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": f"ibapauth=token-{login_count}; Path=/"},
            )
        if request.url.path.endswith("/grid"):
            if grid_401_count == 0:
                grid_401_count += 1
                return json_response({"Error": "Session expired"}, status_code=401)
            return json_response({"_ref": "grid/b25l:Infoblox"})
        return json_response({})

    client = make_http_client(handler)
    try:
        data = await client.request("GET", "/grid")
        assert data == {"_ref": "grid/b25l:Infoblox"}
        assert login_count == 2, "initial login + one re-login"
        assert grid_401_count == 1
    finally:
        await client.aclose()


async def test_second_401_raises_authentication_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        return json_response({"Error": "bad creds"}, status_code=401)

    client = make_http_client(handler)
    try:
        with pytest.raises(AuthenticationError):
            await client.request("GET", "/grid")
    finally:
        await client.aclose()
