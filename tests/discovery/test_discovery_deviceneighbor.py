# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceneighborResource - list, get, find_one, readonly check, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "discovery:deviceneighbor"
REF = f"{WAPI_TYPE}/ZG5z:dn1"


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


async def test_discovery_deviceneighbor_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "nbr1", "address": "10.0.0.2"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.discovery.deviceneighbor.list().all()
        assert len(records) == 1
        assert records[0].name == "nbr1"
        assert records[0].address == "10.0.0.2"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_deviceneighbor_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "nbr1", "device": "disc:device/ZG5z:d1"})
    ) as c:
        r = await c.discovery.deviceneighbor.get(REF)
        assert r.name == "nbr1"


async def test_discovery_deviceneighbor_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "nbr1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.deviceneighbor.find_one()
        assert r is not None
        assert r.name == "nbr1"


async def test_discovery_deviceneighbor_readonly_check() -> None:
    from ibx_nios_sdk.discovery._discovery_deviceneighbor import DiscoveryDeviceneighborResource

    assert "address" in DiscoveryDeviceneighborResource._readonly_fields
    assert "mac" in DiscoveryDeviceneighborResource._readonly_fields


async def test_discovery_deviceneighbor_model_fields() -> None:
    from ibx_nios_sdk.discovery.models.discovery_deviceneighbor import DiscoveryDeviceneighbor

    obj = DiscoveryDeviceneighbor(
        **{"_ref": REF, "name": "nbr1", "address": "10.0.0.2", "mac": "aa:bb:cc:dd:ee:01"}
    )
    assert obj.ref == REF
    assert obj.address == "10.0.0.2"


async def test_discovery_deviceneighbor_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_deviceneighbor import DiscoveryDeviceneighborResource

    assert DiscoveryDeviceneighborResource._wapi_type == "discovery:deviceneighbor"
