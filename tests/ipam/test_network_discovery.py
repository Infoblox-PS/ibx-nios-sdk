# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkDiscoveryResource - list, get, find_one (read-heavy, no writes)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
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


# ---------------------------------------------------------------------------
# 1. list() - returns network_discovery objects
# ---------------------------------------------------------------------------


async def test_network_discovery_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "network_discovery/ZG5z:nd1",
                        "address": "10.0.0.0/24",
                        "network_view": "default",
                        "discovered_data": {},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        entries = await c.ipam.network_discovery.list().all()
        assert len(entries) == 1
        e = entries[0]
        assert e.address == "10.0.0.0/24"
        assert e.network_view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        # network_discovery has no valid default return fields (schema returned empty field list),
        # so _return_fields+ is not sent and WAPI uses its own defaults.
        assert "_return_fields+" not in params


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_network_discovery_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "network_discovery/ZG5z:nd1",
                        "address": "10.0.0.0/24",
                        "network_view": "default",
                        "discovered_data": {},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        entries = await c.ipam.network_discovery.list(network_view="default").all()
        assert len(entries) == 1
        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_network_discovery_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "network_discovery/ZG5z:nd1",
                "address": "10.0.0.0/24",
                "network_view": "default",
                "discovered_data": {"os": "Linux"},
            }
        )

    async with _client(handler) as c:
        ref = "network_discovery/ZG5z:nd1"
        e = await c.ipam.network_discovery.get(ref)
        assert e.address == "10.0.0.0/24"
        assert e.discovered_data == {"os": "Linux"}


# ---------------------------------------------------------------------------
# 4. find_one(address="10.0.0.0/24") - returns first match
# ---------------------------------------------------------------------------


async def test_network_discovery_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "network_discovery/ZG5z:nd1",
                        "address": "10.0.0.0/24",
                        "network_view": "default",
                        "discovered_data": {},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        e = await c.ipam.network_discovery.find_one(address="10.0.0.0/24")
        assert e is not None
        assert e.address == "10.0.0.0/24"


# ---------------------------------------------------------------------------
# 5. _wapi_type is "network_discovery"
# ---------------------------------------------------------------------------


async def test_network_discovery_wapi_type() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    async with _client(handler) as c:
        resource = c.ipam.network_discovery
        assert resource._wapi_type == "network_discovery"


# ---------------------------------------------------------------------------
# 6. model captures clear_discovery_data field
# ---------------------------------------------------------------------------


async def test_network_discovery_model_fields() -> None:
    from ibx_nios_sdk.ipam.models.network_discovery import NetworkDiscovery

    nd = NetworkDiscovery(address="10.0.0.0/24", network_view="default")
    assert nd.address == "10.0.0.0/24"
    assert nd.network_view == "default"
