# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RangeResource - list, get_by_ref, find_one, create, update_strips_readonly, delete, next_available_ip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.range import Range
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "range/ZG5z:10.0.0.100/10.0.0.200/default"
_OBJ = {
    "_ref": _REF,
    "start_addr": "10.0.0.100",
    "end_addr": "10.0.0.200",
    "network": "10.0.0.0/24",
    "network_view": "default",
    "comment": "test range",
    "disable": False,
}


async def test_range_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.range.list().all()
        assert len(results) == 1
        assert results[0].start_addr == "10.0.0.100"
        assert results[0].network == "10.0.0.0/24"
        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "start_addr" in params["_return_fields+"]


async def test_range_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.range.get(_REF)
        assert r.end_addr == "10.0.0.200"
        assert r.network_view == "default"


async def test_range_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.range.find_one(network="10.0.0.0/24")
        assert r is not None
        assert r.start_addr == "10.0.0.100"


async def test_range_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.range.create(
            {"start_addr": "10.0.0.100", "end_addr": "10.0.0.200", "network_view": "default"}
        )
        assert r.start_addr == "10.0.0.100"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert "start_addr" in body
        assert req.url.params.get("_return_as_object") == "1"


async def test_range_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Range(
            start_addr="10.0.0.100",
            end_addr="10.0.0.200",
            comment="updated",
            uuid="some-uuid",  # RO
            dhcp_utilization=50,  # RO
            static_hosts=5,  # RO
        )
        await c.dhcp.range.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "dhcp_utilization" not in body
        assert "static_hosts" not in body
        assert body.get("comment") == "updated"


async def test_range_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.range.delete(_REF)
        assert _REF in result or result == _REF


async def test_range_next_available_ip() -> None:
    captured: list[httpx.Request] = []
    expected_ips = ["10.0.0.105", "10.0.0.106"]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": expected_ips})

    async with _client(handler) as c:
        result = await c.dhcp.range.next_available_ip(_REF, num=2)
        assert result["ips"] == expected_ips
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_function") == "next_available_ip"
        body = json.loads(req.content.decode())
        assert body["num"] == 2


async def test_range_next_available_ip_with_exclude() -> None:
    """Passing exclude must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": ["10.0.0.107"]})

    async with _client(handler) as c:
        result = await c.dhcp.range.next_available_ip(
            _REF, num=1, exclude=["10.0.0.105", "10.0.0.106"]
        )
        assert result["ips"] == ["10.0.0.107"]
        body = json.loads(captured[0].content.decode())
        assert body["exclude"] == ["10.0.0.105", "10.0.0.106"]
