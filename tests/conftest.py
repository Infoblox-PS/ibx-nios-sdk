# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/conftest.py
"""Shared test fixtures and helpers for ibx-nios-sdk tests."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import httpx

from ibx_nios_sdk._http import HttpClient


def json_response(
    payload: Any, status_code: int = 200, headers: dict[str, str] | None = None
) -> httpx.Response:
    """Build an httpx.Response with a JSON body - used in MockTransport handlers."""
    return httpx.Response(
        status_code=status_code,
        content=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **(headers or {})},
    )


Handler = Callable[[httpx.Request], httpx.Response]


def make_http_client(
    handler: Handler,
    *,
    grid_url: str = "https://grid.example.com",
    username: str = "admin",
    password: str = "infoblox",
    wapi_version: str = "2.14",
    use_session: bool = True,
    verify: bool | str = True,
    max_retries: int = 3,
) -> HttpClient:
    """Build an HttpClient backed by an httpx.MockTransport handler."""
    return HttpClient(
        grid_url=grid_url,
        username=username,
        password=password,
        wapi_version=wapi_version,
        use_session=use_session,
        verify=verify,
        max_retries=max_retries,
        transport=httpx.MockTransport(handler),
    )
