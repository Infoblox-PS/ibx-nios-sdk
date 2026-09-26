# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorHttpResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_monitor_http import DtcMonitorHttp
from tests.conftest import json_response

WAPI_TYPE = "dtc:monitor:http"
REF = f"{WAPI_TYPE}/ZG5z:http1"


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


async def test_dtc_monitor_http_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "http1", "port": 80}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.monitor_http.list().all()
        assert len(records) == 1
        assert records[0].name == "http1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_monitor_http_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "http1", "port": 80, "secure": False})
    ) as c:
        r = await c.dtc.monitor_http.get(REF)
        assert r.name == "http1"
        assert r.port == 80


async def test_dtc_monitor_http_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "http1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.monitor_http.find_one(name="http1")
        assert r is not None
        assert r.name == "http1"


async def test_dtc_monitor_http_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "http1"})

    async with _client(handler) as c:
        r = await c.dtc.monitor_http.create({"name": "http1", "port": 80})
        assert r.name == "http1"
        assert captured[0].method == "POST"


async def test_dtc_monitor_http_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "http1"})

    async with _client(handler) as c:
        obj = DtcMonitorHttp(**{"_ref": REF, "name": "http1", "uuid": "ro-uuid"})
        await c.dtc.monitor_http.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"http1"' in body


async def test_dtc_monitor_http_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.monitor_http.delete(REF)
        assert result == REF
