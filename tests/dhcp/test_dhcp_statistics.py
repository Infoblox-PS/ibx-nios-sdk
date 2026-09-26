# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpStatisticsResource - list, get_by_ref, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.dhcp_statistics import DhcpStatistics
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


_REF = "dhcp:statistics/ZG5z:10.0.0.0/24/default"
_OBJ = {
    "_ref": _REF,
    "dhcp_utilization": 75,
    "dhcp_utilization_status": "MEDIUM",
    "dynamic_hosts": 150,
    "static_hosts": 10,
    "total_hosts": 254,
}


async def test_dhcp_statistics_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.dhcp_statistics.list().all()
        assert results[0].dhcp_utilization == 75
        assert "dhcp_utilization" in captured[0].url.params["_return_fields+"]


async def test_dhcp_statistics_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcp_statistics.get(_REF)
        assert r.total_hosts == 254
        assert r.dhcp_utilization_status == "MEDIUM"


async def test_dhcp_statistics_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.dhcp_statistics.find_one()
        assert r is not None
        assert r.dynamic_hosts == 150


async def test_dhcp_statistics_create() -> None:
    """DhcpStatistics is read-only, but the resource layer doesn't prevent creation."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.dhcp_statistics.create({})
        assert r.dhcp_utilization == 75
        assert captured[0].method == "POST"


async def test_dhcp_statistics_update_strips_readonly() -> None:
    """All DhcpStatistics fields are read-only - update body should be empty."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = DhcpStatistics(
            dhcp_utilization=75,
            dynamic_hosts=150,
            static_hosts=10,
            total_hosts=254,
        )
        await c.dhcp.dhcp_statistics.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "dhcp_utilization" not in body
        assert "dynamic_hosts" not in body
        assert "total_hosts" not in body


async def test_dhcp_statistics_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.dhcp_statistics.delete(_REF)
        assert _REF in result or result == _REF
