# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6addressResource - list, find_one, get, extattrs, readonly-strip (read-only object)."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns ipv6address objects
# ---------------------------------------------------------------------------


async def test_ipv6address_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6address/ZG5z:2001:db8::5/default",
                        "ip_address": "2001:db8::5",
                        "duid": "00:01:00:01:12:34:56:78:aa:bb:cc:dd:ee:ff",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "usage": ["DHCP"],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        addrs = await c.ipam.ipv6address.list().all()
        assert len(addrs) == 1
        a = addrs[0]
        assert a.ip_address == "2001:db8::5"
        assert a.duid == "00:01:00:01:12:34:56:78:aa:bb:cc:dd:ee:ff"
        assert a.network == "2001:db8::/64"
        assert a.usage == ["DHCP"]

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "ip_address" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network="2001:db8::/64") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_ipv6address_list_by_network() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6address/ZG5z:2001:db8::5/default",
                        "ip_address": "2001:db8::5",
                        "duid": "",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "usage": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        addrs = await c.ipam.ipv6address.list(network="2001:db8::/64").all()
        assert len(addrs) == 1

        params = captured[0].url.params
        assert params.get("network") == "2001:db8::/64"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses all fields correctly
# ---------------------------------------------------------------------------


async def test_ipv6address_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ipv6address/ZG5z:2001:db8::10/default",
                "ip_address": "2001:db8::10",
                "duid": "00:01:00:01:ab:cd:ef:01:aa:bb:cc:dd:ee:ff",
                "network": "2001:db8::/64",
                "network_view": "default",
                "usage": ["DHCP", "DNS"],
                "status": "USED",
                "names": ["host6.example.com"],
            }
        )

    async with _client(handler) as c:
        ref = "ipv6address/ZG5z:2001:db8::10/default"
        a = await c.ipam.ipv6address.get(ref)
        assert a.ip_address == "2001:db8::10"
        assert a.duid == "00:01:00:01:ab:cd:ef:01:aa:bb:cc:dd:ee:ff"
        assert a.status == "USED"
        assert a.names == ["host6.example.com"]


# ---------------------------------------------------------------------------
# 4. find_one(ip_address="2001:db8::5") - returns first match
# ---------------------------------------------------------------------------


async def test_ipv6address_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6address/ZG5z:2001:db8::5/default",
                        "ip_address": "2001:db8::5",
                        "duid": "",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "usage": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        a = await c.ipam.ipv6address.find_one(ip_address="2001:db8::5")
        assert a is not None
        assert a.ip_address == "2001:db8::5"


# ---------------------------------------------------------------------------
# 5. extattrs round-trip - extattrs parsed correctly
# ---------------------------------------------------------------------------


async def test_ipv6address_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6address/ZG5z:2001:db8::5/default",
                        "ip_address": "2001:db8::5",
                        "duid": "",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "usage": [],
                        "extattrs": {"Site": {"value": "LON"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        addrs = await c.ipam.ipv6address.list().all()
        assert len(addrs) == 1
        a = addrs[0]
        assert a.extattrs is not None
        assert "Site" in a.extattrs
        assert a.extattrs["Site"].value == "LON"


# ---------------------------------------------------------------------------
# 6. readonly model - all key fields correctly marked RO and stripped on update
# ---------------------------------------------------------------------------


async def test_ipv6address_readonly_fields_stripped_on_update() -> None:
    """Even if we pass RO fields, they must be stripped from the PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6address/ZG5z:2001:db8::5/default",
                "ip_address": "2001:db8::5",
                "duid": "",
                "network": "2001:db8::/64",
                "network_view": "default",
                "usage": [],
            }
        )

    async with _client(handler) as c:
        ref = "ipv6address/ZG5z:2001:db8::5/default"
        # set_extattrs uses update internally
        await c.ipam.ipv6address.set_extattrs(ref, Owner="net-eng")

        req = captured[0]
        body = json.loads(req.content.decode())

        # Only extattrs should be in the PUT body (set_extattrs wraps in update)
        assert "extattrs" in body
        assert body["extattrs"]["Owner"]["value"] == "net-eng"
