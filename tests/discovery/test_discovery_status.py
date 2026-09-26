# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryStatusResource - list, get, find_one, type_ alias, readonly, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_status import DiscoveryStatus
from tests.conftest import json_response

WAPI_TYPE = "discovery:status"
REF = f"{WAPI_TYPE}/ZG5z:st1"


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


async def test_discovery_status_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "address": "10.0.0.1", "status": "COMPLETE", "type": "DEVICE"}
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.status.list().all()
        assert len(records) == 1
        assert records[0].address == "10.0.0.1"
        assert records[0].type_ == "DEVICE"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_status_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "address": "10.0.0.1", "status": "COMPLETE"})
    ) as c:
        r = await c.discovery.status.get(REF)
        assert r.address == "10.0.0.1"


async def test_discovery_status_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "address": "10.0.0.1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.status.find_one()
        assert r is not None


async def test_discovery_status_type_alias() -> None:
    obj = DiscoveryStatus(**{"_ref": REF, "type": "NETWORK", "address": "10.0.0.1"})
    assert obj.type_ == "NETWORK"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "type" in dumped
    assert dumped["type"] == "NETWORK"


async def test_discovery_status_readonly_check() -> None:
    from ibx_nios_sdk.discovery._discovery_status import DiscoveryStatusResource

    assert "address" in DiscoveryStatusResource._readonly_fields
    assert "status" in DiscoveryStatusResource._readonly_fields
    assert "type_" in DiscoveryStatusResource._readonly_fields


async def test_discovery_status_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_status import DiscoveryStatusResource

    assert DiscoveryStatusResource._wapi_type == "discovery:status"
