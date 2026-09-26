# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6fixedaddresstemplateResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6fixedaddresstemplate import Ipv6fixedaddresstemplate
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6fixedaddresstemplate/ZG5z:mytemplate"
_OBJ = {
    "_ref": _REF,
    "name": "mytemplate",
    "number_of_addresses": 20,
    "offset": 2,
    "comment": "test ipv6 fa template",
}


async def test_ipv6fixedaddresstemplate_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6fixedaddresstemplate.list().all()
        assert len(results) == 1
        assert results[0].name == "mytemplate"


async def test_ipv6fixedaddresstemplate_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6fixedaddresstemplate.get(_REF)
        assert r.number_of_addresses == 20


async def test_ipv6fixedaddresstemplate_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6fixedaddresstemplate.find_one(name="mytemplate")
        assert r is not None
        assert r.name == "mytemplate"


async def test_ipv6fixedaddresstemplate_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6fixedaddresstemplate.create(
            {"name": "mytemplate", "number_of_addresses": 20}
        )
        assert r.name == "mytemplate"
        assert captured[0].method == "POST"


async def test_ipv6fixedaddresstemplate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6fixedaddresstemplate(name="mytemplate", comment="updated", uuid="some-uuid")
        await c.dhcp.ipv6fixedaddresstemplate.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("comment") == "updated"


async def test_ipv6fixedaddresstemplate_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6fixedaddresstemplate.delete(_REF)
        assert _REF in result or result == _REF
