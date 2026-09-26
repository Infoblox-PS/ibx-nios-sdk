# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorPdpResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_monitor_pdp import DtcMonitorPdp
from tests.conftest import json_response

WAPI_TYPE = "dtc:monitor:pdp"
REF = f"{WAPI_TYPE}/ZG5z:pdp1"


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


async def test_dtc_monitor_pdp_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "pdp1", "port": 3799}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.monitor_pdp.list().all()
        assert len(records) == 1
        assert records[0].name == "pdp1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_monitor_pdp_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "pdp1", "port": 3799})) as c:
        r = await c.dtc.monitor_pdp.get(REF)
        assert r.name == "pdp1"
        assert r.port == 3799


async def test_dtc_monitor_pdp_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "pdp1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.monitor_pdp.find_one(name="pdp1")
        assert r is not None
        assert r.name == "pdp1"


async def test_dtc_monitor_pdp_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "pdp1"})

    async with _client(handler) as c:
        r = await c.dtc.monitor_pdp.create({"name": "pdp1", "port": 3799})
        assert r.name == "pdp1"
        assert captured[0].method == "POST"


async def test_dtc_monitor_pdp_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "pdp1"})

    async with _client(handler) as c:
        obj = DtcMonitorPdp(**{"_ref": REF, "name": "pdp1", "uuid": "ro-uuid"})
        await c.dtc.monitor_pdp.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"pdp1"' in body


async def test_dtc_monitor_pdp_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.monitor_pdp.delete(REF)
        assert result == REF
