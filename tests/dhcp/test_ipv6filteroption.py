# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6filteroptionResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6filteroption import Ipv6filteroption
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6filteroption/ZG5z:myipv6optfilter"
_OBJ = {
    "_ref": _REF,
    "name": "myipv6optfilter",
    "comment": "test ipv6 opt filter",
    "expression": "v6-expr",
}


async def test_ipv6filteroption_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6filteroption.list().all()
        assert results[0].name == "myipv6optfilter"


async def test_ipv6filteroption_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6filteroption.get(_REF)
        assert r.expression == "v6-expr"


async def test_ipv6filteroption_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6filteroption.find_one(name="myipv6optfilter")
        assert r is not None


async def test_ipv6filteroption_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6filteroption.create(
            {"name": "myipv6optfilter", "expression": "v6-expr"}
        )
        assert r.name == "myipv6optfilter"
        assert captured[0].method == "POST"


async def test_ipv6filteroption_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6filteroption(name="myipv6optfilter", comment="updated", uuid="some-uuid")
        await c.dhcp.ipv6filteroption.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("comment") == "updated"


async def test_ipv6filteroption_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6filteroption.delete(_REF)
        assert _REF in result or result == _REF
