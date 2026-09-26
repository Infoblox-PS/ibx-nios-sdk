# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpService wiring: cached_property, shares the HttpClient."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp import DhcpService


def test_dhcp_service_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    assert client.dhcp is client.dhcp, "client.dhcp must be cached"
    assert isinstance(client.dhcp, DhcpService)


def test_dhcp_service_imports() -> None:
    from ibx_nios_sdk.dhcp import DhcpService as _DhcpService  # noqa: F401

    assert _DhcpService is DhcpService
