# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharednetworkResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.sharednetwork import Sharednetwork
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "sharednetwork/ZG5z:myshared/default"
_OBJ = {
    "_ref": _REF,
    "name": "myshared",
    "network_view": "default",
    "networks": ["10.0.0.0/24"],
    "comment": "test shared net",
    "disable": False,
}


async def test_sharednetwork_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.sharednetwork.list().all()
        assert len(results) == 1
        assert results[0].name == "myshared"
        assert "name" in captured[0].url.params["_return_fields+"]


async def test_sharednetwork_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.sharednetwork.get(_REF)
        assert r.network_view == "default"


async def test_sharednetwork_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.sharednetwork.find_one(name="myshared")
        assert r is not None
        assert r.name == "myshared"


async def test_sharednetwork_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.sharednetwork.create(
            {"name": "myshared", "network_view": "default", "networks": ["10.0.0.0/24"]}
        )
        assert r.name == "myshared"
        assert captured[0].method == "POST"


async def test_sharednetwork_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Sharednetwork(
            name="myshared",
            comment="updated",
            uuid="some-uuid",
            dhcp_utilization=80,
            static_hosts=5,
        )
        await c.dhcp.sharednetwork.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "dhcp_utilization" not in body
        assert "static_hosts" not in body
        assert body.get("comment") == "updated"


async def test_sharednetwork_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.sharednetwork.delete(_REF)
        assert _REF in result or result == _REF
