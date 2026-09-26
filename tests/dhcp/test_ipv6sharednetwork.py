# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6sharednetworkResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6sharednetwork import Ipv6sharednetwork
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6sharednetwork/ZG5z:myipv6shared/default"
_OBJ = {
    "_ref": _REF,
    "name": "myipv6shared",
    "network_view": "default",
    "networks": ["2001:db8::/32"],
    "comment": "test ipv6 shared net",
    "disable": False,
}


async def test_ipv6sharednetwork_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6sharednetwork.list().all()
        assert len(results) == 1
        assert results[0].name == "myipv6shared"
        assert "name" in captured[0].url.params["_return_fields+"]


async def test_ipv6sharednetwork_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6sharednetwork.get(_REF)
        assert r.network_view == "default"


async def test_ipv6sharednetwork_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6sharednetwork.find_one(name="myipv6shared")
        assert r is not None
        assert r.name == "myipv6shared"


async def test_ipv6sharednetwork_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6sharednetwork.create(
            {"name": "myipv6shared", "network_view": "default", "networks": ["2001:db8::/32"]}
        )
        assert r.name == "myipv6shared"
        assert captured[0].method == "POST"


async def test_ipv6sharednetwork_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6sharednetwork(name="myipv6shared", comment="updated", uuid="some-uuid")
        await c.dhcp.ipv6sharednetwork.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("comment") == "updated"


async def test_ipv6sharednetwork_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6sharednetwork.delete(_REF)
        assert _REF in result or result == _REF
