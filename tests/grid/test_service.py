# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridService wiring: cached_property, shares the HttpClient."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid import GridService


def test_grid_service_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    assert client.grid is client.grid, "client.grid must be cached"
    assert isinstance(client.grid, GridService)


def test_grid_service_imports() -> None:
    from ibx_nios_sdk.grid import GridService as _GridService  # noqa: F401

    assert _GridService is GridService
