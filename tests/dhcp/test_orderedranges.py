# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""OrderedrangesResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.orderedranges import Orderedranges
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


_REF = "orderedranges/ZG5z:10.0.0.0/24/default"
_OBJ = {
    "_ref": _REF,
    "network": "10.0.0.0/24",
    "ranges": ["range/ZG5z:10.0.0.100/10.0.0.200/default"],
}


async def test_orderedranges_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.orderedranges.list().all()
        assert len(results) == 1
        assert results[0].network == "10.0.0.0/24"
        assert "network" in captured[0].url.params["_return_fields+"]


async def test_orderedranges_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.orderedranges.get(_REF)
        assert r.network == "10.0.0.0/24"
        assert len(r.ranges) == 1  # type: ignore[arg-type]


async def test_orderedranges_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.orderedranges.find_one(network="10.0.0.0/24")
        assert r is not None
        assert r.network == "10.0.0.0/24"


async def test_orderedranges_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.orderedranges.create(
            {"ranges": ["range/ZG5z:10.0.0.100/10.0.0.200/default"]}
        )
        assert r.ranges is not None
        assert captured[0].method == "POST"


async def test_orderedranges_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Orderedranges(
            network="10.0.0.0/24",  # RO
            ranges=["range/ZG5z:10.0.0.100/10.0.0.200/default"],
        )
        await c.dhcp.orderedranges.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "network" not in body  # read-only stripped


async def test_orderedranges_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.orderedranges.delete(_REF)
        assert _REF in result or result == _REF
