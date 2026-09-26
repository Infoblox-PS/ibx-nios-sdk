# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IpamService wiring: cached_property, shares the HttpClient."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam import IpamService


def test_ipam_service_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    assert client.ipam is client.ipam, "client.ipam must be cached"
    assert isinstance(client.ipam, IpamService)


def test_ipam_service_imports() -> None:
    from ibx_nios_sdk.ipam import IpamService as _IpamService  # noqa: F401

    assert _IpamService is IpamService
