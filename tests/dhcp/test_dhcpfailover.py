# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpfailoverResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.dhcpfailover import Dhcpfailover
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "dhcpfailover/ZG5z:myfailover"
_OBJ = {
    "_ref": _REF,
    "name": "myfailover",
    "primary": "192.168.1.1",
    "secondary": "192.168.1.2",
    "comment": "test failover",
}


async def test_dhcpfailover_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.dhcpfailover.list().all()
        assert results[0].name == "myfailover"
        assert "name" in captured[0].url.params["_return_fields+"]


async def test_dhcpfailover_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcpfailover.get(_REF)
        assert r.primary == "192.168.1.1"


async def test_dhcpfailover_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.dhcpfailover.find_one(name="myfailover")
        assert r is not None


async def test_dhcpfailover_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcpfailover.create(
            {"name": "myfailover", "primary": "192.168.1.1", "secondary": "192.168.1.2"}
        )
        assert r.name == "myfailover"
        assert captured[0].method == "POST"


async def test_dhcpfailover_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Dhcpfailover(
            name="myfailover",
            comment="updated",
            uuid="some-uuid",
            association_type="FAILOVER",
            primary_state="NORMAL",
        )
        await c.dhcp.dhcpfailover.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "association_type" not in body
        assert "primary_state" not in body
        assert body.get("comment") == "updated"


async def test_dhcpfailover_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.dhcpfailover.delete(_REF)
        assert _REF in result or result == _REF
