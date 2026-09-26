# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6dhcpoptiondefinitionResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6dhcpoptiondefinition import Ipv6dhcpoptiondefinition
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6dhcpoptiondefinition/ZG5z:myipv6opt/DHCPv6"
_OBJ = {
    "_ref": _REF,
    "name": "myipv6opt",
    "code": 100,
    "space": "DHCPv6",
    "type": "string",
}


async def test_ipv6dhcpoptiondefinition_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6dhcpoptiondefinition.list().all()
        assert results[0].name == "myipv6opt"
        assert results[0].type_ == "string"


async def test_ipv6dhcpoptiondefinition_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6dhcpoptiondefinition.get(_REF)
        assert r.code == 100


async def test_ipv6dhcpoptiondefinition_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6dhcpoptiondefinition.find_one(name="myipv6opt")
        assert r is not None


async def test_ipv6dhcpoptiondefinition_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6dhcpoptiondefinition.create({"name": "myipv6opt", "code": 100})
        assert r.name == "myipv6opt"
        assert captured[0].method == "POST"


async def test_ipv6dhcpoptiondefinition_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6dhcpoptiondefinition(name="myipv6opt", uuid="some-uuid")
        await c.dhcp.ipv6dhcpoptiondefinition.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body


async def test_ipv6dhcpoptiondefinition_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6dhcpoptiondefinition.delete(_REF)
        assert _REF in result or result == _REF
