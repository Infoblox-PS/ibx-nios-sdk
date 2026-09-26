# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDiagnostictaskResource - list, get, find_one, update, readonly, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_diagnostictask import DiscoveryDiagnostictask
from tests.conftest import json_response

WAPI_TYPE = "discovery:diagnostictask"
REF = f"{WAPI_TYPE}/ZG5z:dt1"


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


async def test_discovery_diagnostictask_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "ip_address": "10.0.0.5", "network_view": "default"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.diagnostictask.list().all()
        assert len(records) == 1
        assert records[0].ip_address == "10.0.0.5"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_diagnostictask_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "ip_address": "10.0.0.5", "task_id": "tid1"})
    ) as c:
        r = await c.discovery.diagnostictask.get(REF)
        assert r.ip_address == "10.0.0.5"
        assert r.task_id == "tid1"


async def test_discovery_diagnostictask_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "ip_address": "10.0.0.5"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.diagnostictask.find_one()
        assert r is not None


async def test_discovery_diagnostictask_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DiscoveryDiagnostictask(
            **{
                "_ref": REF,
                "ip_address": "10.0.0.5",
                "network_view": "default",
                "task_id": "ro-tid",
                "uuid": "ro-uuid",
                "start_time": 12345,
                "debug_snmp": True,
            }
        )
        await c.discovery.diagnostictask.update(REF, obj)
        body = captured[0].content.decode()
        assert '"task_id"' not in body, "task_id is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"start_time"' not in body, "start_time is readonly - must be stripped"
        assert "true" in body.lower()  # debug_snmp


async def test_discovery_diagnostictask_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_diagnostictask import DiscoveryDiagnostictaskResource

    assert DiscoveryDiagnostictaskResource._wapi_type == "discovery:diagnostictask"
