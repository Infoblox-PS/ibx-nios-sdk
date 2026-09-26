# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MacfilteraddressResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.macfilteraddress import Macfilteraddress
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "macfilteraddress/ZG5z:aa:bb:cc:dd:ee:ff/mymacfilter"
_OBJ = {
    "_ref": _REF,
    "mac": "aa:bb:cc:dd:ee:ff",
    "filter": "mymacfilter",
    "comment": "test mac filter addr",
}


async def test_macfilteraddress_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.macfilteraddress.list().all()
        assert results[0].mac == "aa:bb:cc:dd:ee:ff"
        assert "mac" in captured[0].url.params["_return_fields+"]


async def test_macfilteraddress_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.macfilteraddress.get(_REF)
        assert r.filter == "mymacfilter"


async def test_macfilteraddress_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.macfilteraddress.find_one(mac="aa:bb:cc:dd:ee:ff")
        assert r is not None


async def test_macfilteraddress_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.macfilteraddress.create(
            {"mac": "aa:bb:cc:dd:ee:ff", "filter": "mymacfilter"}
        )
        assert r.mac == "aa:bb:cc:dd:ee:ff"
        assert captured[0].method == "POST"


async def test_macfilteraddress_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Macfilteraddress(
            mac="aa:bb:cc:dd:ee:ff",
            comment="updated",
            uuid="some-uuid",
            fingerprint="fp",
            is_registered_user=True,
        )
        await c.dhcp.macfilteraddress.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "fingerprint" not in body
        assert "is_registered_user" not in body
        assert body.get("comment") == "updated"


async def test_macfilteraddress_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.macfilteraddress.delete(_REF)
        assert _REF in result or result == _REF
