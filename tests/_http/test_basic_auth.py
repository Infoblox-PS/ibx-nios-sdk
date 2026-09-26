# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_basic_auth.py
"""Basic-auth mode: no login call, credentials sent per request via httpx BasicAuth."""

from __future__ import annotations

import base64

import httpx

from tests.conftest import json_response, make_http_client


async def test_basic_auth_mode_skips_login() -> None:
    paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        auth = request.headers.get("Authorization", "")
        assert auth.startswith("Basic ")
        decoded = base64.b64decode(auth.removeprefix("Basic ")).decode()
        assert decoded == "admin:infoblox"
        return json_response({"_ref": "grid/x:g"})

    client = make_http_client(handler, use_session=False)
    try:
        await client.request("GET", "/grid")
        assert not any(p.endswith("/?_schema=1") for p in paths)
    finally:
        await client.aclose()
