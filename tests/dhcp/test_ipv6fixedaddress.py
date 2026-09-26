# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6fixedaddressResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6fixedaddress import Ipv6fixedaddress
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6fixedaddress/ZG5z:2001:db8::5/default"
_OBJ = {
    "_ref": _REF,
    "ipv6addr": "2001:db8::5",
    "duid": "00:01:00:01:aa:bb:cc:dd:ee:ff",
    "name": "myipv6host",
    "network": "2001:db8::/32",
    "network_view": "default",
    "comment": "test ipv6 fixed",
}


async def test_ipv6fixedaddress_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6fixedaddress.list().all()
        assert len(results) == 1
        assert results[0].ipv6addr == "2001:db8::5"
        assert "ipv6addr" in captured[0].url.params["_return_fields+"]


async def test_ipv6fixedaddress_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6fixedaddress.get(_REF)
        assert r.duid == "00:01:00:01:aa:bb:cc:dd:ee:ff"


async def test_ipv6fixedaddress_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6fixedaddress.find_one(ipv6addr="2001:db8::5")
        assert r is not None
        assert r.network == "2001:db8::/32"


async def test_ipv6fixedaddress_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6fixedaddress.create(
            {"ipv6addr": "2001:db8::5", "duid": "00:01:00:01:aa:bb:cc:dd:ee:ff"}
        )
        assert r.ipv6addr == "2001:db8::5"
        assert captured[0].method == "POST"


async def test_ipv6fixedaddress_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6fixedaddress(
            ipv6addr="2001:db8::5",
            comment="updated",
            uuid="ro-uuid",
            discover_now_status="IDLE",
        )
        await c.dhcp.ipv6fixedaddress.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "discover_now_status" not in body
        assert body.get("comment") == "updated"


async def test_ipv6fixedaddress_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6fixedaddress.delete(_REF)
        assert _REF in result or result == _REF
