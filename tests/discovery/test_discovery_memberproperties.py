# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryMemberpropertiesResource - list, get, find_one, update, readonly, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_memberproperties import DiscoveryMemberproperties
from tests.conftest import json_response

WAPI_TYPE = "discovery:memberproperties"
REF = f"{WAPI_TYPE}/ZG5z:mp1"


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


async def test_discovery_memberproperties_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "discovery_member": "m1.example.com", "role": "MASTER"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.memberproperties.list().all()
        assert len(records) == 1
        assert records[0].discovery_member == "m1.example.com"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_memberproperties_get() -> None:
    async with _client(
        _session_handler(
            {"_ref": REF, "discovery_member": "m1.example.com", "address": "10.0.0.1"}
        )
    ) as c:
        r = await c.discovery.memberproperties.get(REF)
        assert r.discovery_member == "m1.example.com"


async def test_discovery_memberproperties_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "discovery_member": "m1.example.com"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.discovery.memberproperties.find_one()
        assert r is not None


async def test_discovery_memberproperties_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DiscoveryMemberproperties(
            **{
                "_ref": REF,
                "address": "10.0.0.1",
                "is_sa": True,
                "role": "MASTER",
                "uuid": "ro-uuid",
                "enable_service": True,
                "discovery_member": "m1.example.com",
            }
        )
        await c.discovery.memberproperties.update(REF, obj)
        body = captured[0].content.decode()
        assert '"address"' not in body, "address is readonly - must be stripped"
        assert '"is_sa"' not in body, "is_sa is readonly - must be stripped"
        assert '"role"' not in body, "role is readonly - must be stripped"
        assert "true" in body.lower()  # enable_service


async def test_discovery_memberproperties_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_memberproperties import (
        DiscoveryMemberpropertiesResource,
    )

    assert DiscoveryMemberpropertiesResource._wapi_type == "discovery:memberproperties"
