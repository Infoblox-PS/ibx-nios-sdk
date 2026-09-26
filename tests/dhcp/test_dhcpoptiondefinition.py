# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpoptiondefinitionResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.dhcpoptiondefinition import Dhcpoptiondefinition
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "dhcpoptiondefinition/ZG5z:myopt/DHCP"
_OBJ = {
    "_ref": _REF,
    "name": "myopt",
    "code": 240,
    "space": "DHCP",
    "type": "string",
}


async def test_dhcpoptiondefinition_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.dhcpoptiondefinition.list().all()
        assert results[0].name == "myopt"
        assert results[0].type_ == "string"
        assert "name" in captured[0].url.params["_return_fields+"]


async def test_dhcpoptiondefinition_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcpoptiondefinition.get(_REF)
        assert r.code == 240
        assert r.type_ == "string"


async def test_dhcpoptiondefinition_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.dhcpoptiondefinition.find_one(name="myopt")
        assert r is not None
        assert r.space == "DHCP"


async def test_dhcpoptiondefinition_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcpoptiondefinition.create(
            {"name": "myopt", "code": 240, "space": "DHCP", "type": "string"}
        )
        assert r.name == "myopt"
        assert captured[0].method == "POST"


async def test_dhcpoptiondefinition_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Dhcpoptiondefinition(name="myopt", uuid="some-uuid")
        await c.dhcp.dhcpoptiondefinition.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("name") == "myopt"


async def test_dhcpoptiondefinition_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.dhcpoptiondefinition.delete(_REF)
        assert _REF in result or result == _REF
