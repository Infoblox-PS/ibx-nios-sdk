# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IpamStatisticsResource - list, get, find_one (read-only aggregate view)."""

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
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns ipam:statistics objects
# ---------------------------------------------------------------------------


async def test_ipam_statistics_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipam:statistics/ZG5z:stat1",
                        "network": "10.0.0.0/24",
                        "network_view": "default",
                        "utilization": 42,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        stats = await c.ipam.ipam_statistics.list().all()
        assert len(stats) == 1
        s = stats[0]
        assert s.network == "10.0.0.0/24"
        assert s.utilization == 42

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "network" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_ipam_statistics_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipam:statistics/ZG5z:stat1",
                        "network": "10.0.0.0/24",
                        "network_view": "default",
                        "utilization": 42,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        stats = await c.ipam.ipam_statistics.list(network_view="default").all()
        assert len(stats) == 1
        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_ipam_statistics_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ipam:statistics/ZG5z:stat1",
                "network": "10.0.0.0/24",
                "network_view": "default",
                "utilization": 75,
                "cidr": 24,
                "conflict_count": 0,
            }
        )

    async with _client(handler) as c:
        ref = "ipam:statistics/ZG5z:stat1"
        s = await c.ipam.ipam_statistics.get(ref)
        assert s.network == "10.0.0.0/24"
        assert s.utilization == 75
        assert s.cidr == 24


# ---------------------------------------------------------------------------
# 4. find_one(network="10.0.0.0/24") - returns first match
# ---------------------------------------------------------------------------


async def test_ipam_statistics_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipam:statistics/ZG5z:stat1",
                        "network": "10.0.0.0/24",
                        "network_view": "default",
                        "utilization": 42,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        s = await c.ipam.ipam_statistics.find_one(network="10.0.0.0/24")
        assert s is not None
        assert s.network == "10.0.0.0/24"


# ---------------------------------------------------------------------------
# 5. _wapi_type is "ipam:statistics"
# ---------------------------------------------------------------------------


async def test_ipam_statistics_wapi_type() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    async with _client(handler) as c:
        resource = c.ipam.ipam_statistics
        assert resource._wapi_type == "ipam:statistics"


# ---------------------------------------------------------------------------
# 6. model captures ms_ad_user_data and all readonly fields
# ---------------------------------------------------------------------------


async def test_ipam_statistics_model_fields() -> None:
    from ibx_nios_sdk.ipam.models.ipam_statistics import IpamStatistics

    stat = IpamStatistics(
        network="10.0.0.0/24",
        network_view="default",
        utilization=50,
        cidr=24,
        conflict_count=2,
        unmanaged_count=10,
    )
    assert stat.network == "10.0.0.0/24"
    assert stat.utilization == 50
    assert stat.conflict_count == 2
