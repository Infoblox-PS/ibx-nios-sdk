# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LeaseResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.lease import Lease
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


_REF = "lease/ZG5z:10.0.0.5"
_OBJ = {
    "_ref": _REF,
    "address": "10.0.0.5",
    "hardware": "aa:bb:cc:dd:ee:ff",
    "client_hostname": "myhost",
    "binding_state": "ACTIVE",
}


async def test_lease_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.lease.list().all()
        assert results[0].address == "10.0.0.5"
        assert "address" in captured[0].url.params["_return_fields+"]


async def test_lease_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.lease.get(_REF)
        assert r.binding_state == "ACTIVE"


async def test_lease_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.lease.find_one(address="10.0.0.5")
        assert r is not None
        assert r.client_hostname == "myhost"


async def test_lease_create() -> None:
    """Lease is read-only, but the resource layer doesn't prevent creation."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.lease.create({"address": "10.0.0.5"})
        assert r.address == "10.0.0.5"
        assert captured[0].method == "POST"


async def test_lease_update_strips_readonly() -> None:
    """All lease fields are read-only - the update body should be empty."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Lease(
            address="10.0.0.5",
            binding_state="ACTIVE",
            hardware="aa:bb:cc:dd:ee:ff",
            client_hostname="myhost",
        )
        await c.dhcp.lease.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        # All fields stripped - body should be empty or have no RO fields
        assert "address" not in body
        assert "binding_state" not in body
        assert "hardware" not in body


async def test_lease_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.lease.delete(_REF)
        assert _REF in result or result == _REF
