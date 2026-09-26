# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoverySdnnetworkResource - list, get, find_one, readonly, model, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "discovery:sdnnetwork"
REF = f"{WAPI_TYPE}/ZG5z:sdn1"


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


async def test_discovery_sdnnetwork_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "sdn1", "network_view": "default"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.sdnnetwork.list().all()
        assert len(records) == 1
        assert records[0].name == "sdn1"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_sdnnetwork_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "sdn1", "source_sdn_config": "sdn-cfg"})
    ) as c:
        r = await c.discovery.sdnnetwork.get(REF)
        assert r.name == "sdn1"


async def test_discovery_sdnnetwork_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "sdn1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.sdnnetwork.find_one()
        assert r is not None


async def test_discovery_sdnnetwork_readonly_check() -> None:
    from ibx_nios_sdk.discovery._discovery_sdnnetwork import DiscoverySdnnetworkResource

    assert "name" in DiscoverySdnnetworkResource._readonly_fields
    assert "network_view" in DiscoverySdnnetworkResource._readonly_fields
    assert "first_seen" in DiscoverySdnnetworkResource._readonly_fields


async def test_discovery_sdnnetwork_model_fields() -> None:
    from ibx_nios_sdk.discovery.models.discovery_sdnnetwork import DiscoverySdnnetwork

    obj = DiscoverySdnnetwork(**{"_ref": REF, "name": "sdn1", "first_seen": 1700000000})
    assert obj.name == "sdn1"
    assert obj.first_seen == 1700000000


async def test_discovery_sdnnetwork_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_sdnnetwork import DiscoverySdnnetworkResource

    assert DiscoverySdnnetworkResource._wapi_type == "discovery:sdnnetwork"
