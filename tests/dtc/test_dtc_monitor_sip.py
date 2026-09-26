# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorSipResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_monitor_sip import DtcMonitorSip
from tests.conftest import json_response

WAPI_TYPE = "dtc:monitor:sip"
REF = f"{WAPI_TYPE}/ZG5z:sip1"


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


async def test_dtc_monitor_sip_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "sip1", "port": 5060}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.monitor_sip.list().all()
        assert len(records) == 1
        assert records[0].name == "sip1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_monitor_sip_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "sip1", "port": 5060, "transport": "UDP"})
    ) as c:
        r = await c.dtc.monitor_sip.get(REF)
        assert r.name == "sip1"
        assert r.transport == "UDP"


async def test_dtc_monitor_sip_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "sip1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.monitor_sip.find_one(name="sip1")
        assert r is not None
        assert r.name == "sip1"


async def test_dtc_monitor_sip_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "sip1"})

    async with _client(handler) as c:
        r = await c.dtc.monitor_sip.create({"name": "sip1", "port": 5060})
        assert r.name == "sip1"
        assert captured[0].method == "POST"


async def test_dtc_monitor_sip_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "sip1"})

    async with _client(handler) as c:
        obj = DtcMonitorSip(**{"_ref": REF, "name": "sip1", "uuid": "ro-uuid"})
        await c.dtc.monitor_sip.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"sip1"' in body


async def test_dtc_monitor_sip_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.monitor_sip.delete(REF)
        assert result == REF
