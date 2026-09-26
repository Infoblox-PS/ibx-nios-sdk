# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionStatisticsResource - list, get, find_one, model_roundtrip, readonly_strip, type_check."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_statistics import (
    ThreatprotectionStatistics,
)
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:statistics"
REF = f"{WAPI_TYPE}/ZG5z:gm.example.com"
MEMBER_REF = "member:grid/ZG5z:gm.example.com"


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


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


# 1. list
async def test_statistics_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": REF,
                        "member": MEMBER_REF,
                        "stat_infos": [{"timestamp": 1700000000, "total": {"count": 5}}],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.statistics.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.member == MEMBER_REF
        assert r.stat_infos is not None
        assert len(r.stat_infos) == 1
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_statistics_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "member": MEMBER_REF,
                "stat_infos": [
                    {
                        "timestamp": 1700000000,
                        "critical": {"count": 0},
                        "total": {"count": 10},
                    }
                ],
            }
        )
    ) as c:
        r = await c.threatprotection.statistics.get(REF)
        assert r.member == MEMBER_REF
        assert r.stat_infos is not None
        assert r.stat_infos[0]["timestamp"] == 1700000000


# 3. find_one
async def test_statistics_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "member": MEMBER_REF,
                        "stat_infos": [],
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.statistics.find_one(member=MEMBER_REF)
        assert r is not None
        assert r.member == MEMBER_REF


# 4. model roundtrip validates stat_infos array
async def test_statistics_model_roundtrip() -> None:
    data = {
        "_ref": REF,
        "member": MEMBER_REF,
        "stat_infos": [
            {
                "timestamp": 1700000000,
                "critical": {"count": 2, "bytes": 100},
                "major": {"count": 1, "bytes": 50},
                "warning": {"count": 0, "bytes": 0},
                "informational": {"count": 3, "bytes": 200},
                "total": {"count": 6, "bytes": 350},
            }
        ],
    }
    obj = ThreatprotectionStatistics.model_validate(data)
    assert obj.member == MEMBER_REF
    assert obj.stat_infos is not None
    assert obj.stat_infos[0]["timestamp"] == 1700000000
    assert obj.stat_infos[0]["critical"]["count"] == 2


# 5. update strips all readonly fields (member, stat_infos)
async def test_statistics_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "member": MEMBER_REF,
                "stat_infos": [],
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionStatistics.model_validate(
            {"member": MEMBER_REF, "stat_infos": [{"timestamp": 1700000000}]}
        )
        await c.threatprotection.statistics.update(REF, obj)
        body = captured[0].content.decode()
        assert '"member"' not in body, "member is readonly - must be stripped"
        assert '"stat_infos"' not in body, "stat_infos is readonly - must be stripped"


# 6. resource is accessible as cached property on service
async def test_statistics_resource_type() -> None:
    from ibx_nios_sdk.threatprotection._statistics import ThreatprotectionStatisticsResource

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({})

    c = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )
    assert isinstance(c.threatprotection.statistics, ThreatprotectionStatisticsResource)
