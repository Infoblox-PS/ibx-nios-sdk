# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryVrfResource - list, get, find_one, readonly, model, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "discovery:vrf"
REF = f"{WAPI_TYPE}/ZG5z:vrf1"


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


async def test_discovery_vrf_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "vrf1", "route_distinguisher": "100:1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.vrf.list().all()
        assert len(records) == 1
        assert records[0].name == "vrf1"
        assert records[0].route_distinguisher == "100:1"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_vrf_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "vrf1", "device": "disc:device/ZG5z:d1"})
    ) as c:
        r = await c.discovery.vrf.get(REF)
        assert r.name == "vrf1"


async def test_discovery_vrf_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "vrf1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.vrf.find_one(name="vrf1")
        assert r is not None


async def test_discovery_vrf_readonly_check() -> None:
    from ibx_nios_sdk.discovery._discovery_vrf import DiscoveryVrfResource

    assert "name" in DiscoveryVrfResource._readonly_fields
    assert "device" in DiscoveryVrfResource._readonly_fields
    assert "network_view" in DiscoveryVrfResource._readonly_fields


async def test_discovery_vrf_model_fields() -> None:
    from ibx_nios_sdk.discovery.models.discovery_vrf import DiscoveryVrf

    obj = DiscoveryVrf(
        **{
            "_ref": REF,
            "name": "vrf1",
            "description": "VRF for corp",
            "route_distinguisher": "100:1",
        }
    )
    assert obj.description == "VRF for corp"


async def test_discovery_vrf_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_vrf import DiscoveryVrfResource

    assert DiscoveryVrfResource._wapi_type == "discovery:vrf"
