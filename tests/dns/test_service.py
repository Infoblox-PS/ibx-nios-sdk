# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DnsService wiring: cached_property per resource, shares the HttpClient."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns import DnsService, RecordAResource, ViewResource, ZoneAuthResource


def test_dns_service_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    svc1 = client.dns
    svc2 = client.dns
    assert svc1 is svc2, "client.dns must be cached"
    assert isinstance(svc1, DnsService)


def test_dns_resources_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    dns = client.dns
    assert isinstance(dns.view, ViewResource)
    assert isinstance(dns.zone_auth, ZoneAuthResource)
    assert isinstance(dns.record_a, RecordAResource)

    # caching
    assert dns.view is dns.view
    assert dns.zone_auth is dns.zone_auth
    assert dns.record_a is dns.record_a
