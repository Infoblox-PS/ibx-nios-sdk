# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6rangeResource - list, get_by_ref, find_one, create, update_strips_readonly, delete, next_available_ip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dhcp.models.ipv6range import Ipv6range
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


_REF = "ipv6range/ZG5z:2001:db8::/2001:db8::100/default"
_OBJ = {
    "_ref": _REF,
    "start_addr": "2001:db8::100",
    "end_addr": "2001:db8::200",
    "network": "2001:db8::/32",
    "network_view": "default",
    "comment": "test ipv6 range",
    "disable": False,
}


async def test_ipv6range_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.dhcp.ipv6range.list().all()
        assert len(results) == 1
        assert results[0].start_addr == "2001:db8::100"
        assert "start_addr" in captured[0].url.params["_return_fields+"]


async def test_ipv6range_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6range.get(_REF)
        assert r.end_addr == "2001:db8::200"


async def test_ipv6range_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dhcp.ipv6range.find_one(network="2001:db8::/32")
        assert r is not None
        assert r.network == "2001:db8::/32"


async def test_ipv6range_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = await c.dhcp.ipv6range.create(
            {"start_addr": "2001:db8::100", "end_addr": "2001:db8::200"}
        )
        assert r.start_addr == "2001:db8::100"
        assert captured[0].method == "POST"


async def test_ipv6range_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_OBJ)

    async with _client(handler) as c:
        r = Ipv6range(
            start_addr="2001:db8::100",
            comment="updated",
            uuid="ro-uuid",
            discover_now_status="IDLE",
        )
        await c.dhcp.ipv6range.update(_REF, r)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "discover_now_status" not in body
        assert body.get("comment") == "updated"


async def test_ipv6range_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dhcp.ipv6range.delete(_REF)
        assert _REF in result or result == _REF


async def test_ipv6range_next_available_ip() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": ["2001:db8::101"]})

    async with _client(handler) as c:
        result = await c.dhcp.ipv6range.next_available_ip(_REF, num=1)
        assert result["ips"] == ["2001:db8::101"]
        assert captured[0].url.params.get("_function") == "next_available_ip"


async def test_ipv6range_next_available_ip_with_exclude() -> None:
    """Passing exclude must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": ["2001:db8::102"]})

    async with _client(handler) as c:
        result = await c.dhcp.ipv6range.next_available_ip(_REF, num=1, exclude=["2001:db8::101"])
        assert result["ips"] == ["2001:db8::102"]
        body = json.loads(captured[0].content.decode())
        assert body["exclude"] == ["2001:db8::101"]
