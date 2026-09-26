# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpoptionspaceResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.dhcpoptionspace import Dhcpoptionspace
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "dhcpoptionspace/ZG5z:myoptspace"
_OBJ = {
    "_ref": _REF,
    "name": "myoptspace",
    "comment": "test option space",
    "space_type": "DHCP",
}


async def test_dhcpoptionspace_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.dhcpoptionspace.list().all()
        assert results[0].name == "myoptspace"


async def test_dhcpoptionspace_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcpoptionspace.get(_REF)
        assert r.space_type == "DHCP"


async def test_dhcpoptionspace_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.dhcpoptionspace.find_one(name="myoptspace")
        assert r is not None


async def test_dhcpoptionspace_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcpoptionspace.create({"name": "myoptspace"})
        assert r.name == "myoptspace"
        assert captured[0].method == "POST"


async def test_dhcpoptionspace_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Dhcpoptionspace(
            name="myoptspace", comment="updated", uuid="some-uuid", space_type="DHCP"
        )
        await c.dhcp.dhcpoptionspace.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "space_type" not in body
        assert body.get("comment") == "updated"


async def test_dhcpoptionspace_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.dhcpoptionspace.delete(_REF)
        assert _REF in result or result == _REF
