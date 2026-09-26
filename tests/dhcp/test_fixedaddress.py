# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FixedaddressResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.fixedaddress import Fixedaddress
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "fixedaddress/ZG5z:10.0.0.5/default"
_OBJ = {
    "_ref": _REF,
    "ipv4addr": "10.0.0.5",
    "mac": "aa:bb:cc:dd:ee:ff",
    "name": "myhost",
    "network": "10.0.0.0/24",
    "network_view": "default",
    "comment": "test fixed",
}


async def test_fixedaddress_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.fixedaddress.list().all()
        assert len(results) == 1
        assert results[0].ipv4addr == "10.0.0.5"
        assert "ipv4addr" in captured[0].url.params["_return_fields+"]


async def test_fixedaddress_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.fixedaddress.get(_REF)
        assert r.mac == "aa:bb:cc:dd:ee:ff"


async def test_fixedaddress_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.fixedaddress.find_one(ipv4addr="10.0.0.5")
        assert r is not None
        assert r.ipv4addr == "10.0.0.5"


async def test_fixedaddress_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.fixedaddress.create({"ipv4addr": "10.0.0.5", "mac": "aa:bb:cc:dd:ee:ff"})
        assert r.ipv4addr == "10.0.0.5"
        assert captured[0].method == "POST"


async def test_fixedaddress_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Fixedaddress(
            ipv4addr="10.0.0.5",
            comment="updated",
            uuid="some-uuid",
            is_invalid_mac=True,
            discover_now_status="IDLE",
        )
        await c.dhcp.fixedaddress.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "is_invalid_mac" not in body
        assert "discover_now_status" not in body
        assert body.get("comment") == "updated"


async def test_fixedaddress_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.fixedaddress.delete(_REF)
        assert _REF in result or result == _REF
