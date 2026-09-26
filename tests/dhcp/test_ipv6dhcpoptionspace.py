# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6dhcpoptionspaceResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6dhcpoptionspace import Ipv6dhcpoptionspace
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6dhcpoptionspace/ZG5z:myipv6optspace"
_OBJ = {
    "_ref": _REF,
    "name": "myipv6optspace",
    "comment": "test ipv6 option space",
    "enterprise_number": 12345,
}


async def test_ipv6dhcpoptionspace_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6dhcpoptionspace.list().all()
        assert results[0].name == "myipv6optspace"


async def test_ipv6dhcpoptionspace_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6dhcpoptionspace.get(_REF)
        assert r.enterprise_number == 12345


async def test_ipv6dhcpoptionspace_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6dhcpoptionspace.find_one(name="myipv6optspace")
        assert r is not None


async def test_ipv6dhcpoptionspace_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6dhcpoptionspace.create(
            {"name": "myipv6optspace", "enterprise_number": 12345}
        )
        assert r.name == "myipv6optspace"
        assert captured[0].method == "POST"


async def test_ipv6dhcpoptionspace_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6dhcpoptionspace(name="myipv6optspace", comment="updated", uuid="some-uuid")
        await c.dhcp.ipv6dhcpoptionspace.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("comment") == "updated"


async def test_ipv6dhcpoptionspace_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6dhcpoptionspace.delete(_REF)
        assert _REF in result or result == _REF
