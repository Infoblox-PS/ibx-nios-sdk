# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorResource - list, get, find_one, update, type_ alias, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_monitor import DtcMonitor
from tests.conftest import json_response

WAPI_TYPE = "dtc:monitor"
REF = f"{WAPI_TYPE}/ZG5z:mon1"


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


async def test_dtc_monitor_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "mon1", "type": "HTTP"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.monitor.list().all()
        assert len(records) == 1
        assert records[0].name == "mon1"
        assert records[0].type_ == "HTTP"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_monitor_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "mon1", "type": "ICMP"})) as c:
        r = await c.dtc.monitor.get(REF)
        assert r.name == "mon1"
        assert r.type_ == "ICMP"


async def test_dtc_monitor_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "mon1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.monitor.find_one(name="mon1")
        assert r is not None
        assert r.name == "mon1"


async def test_dtc_monitor_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "mon1"})

    async with _client(handler) as c:
        r = await c.dtc.monitor.update(REF, {"interval": 30})
        assert r.ref == REF
        assert captured[0].method == "PUT"


async def test_dtc_monitor_type_alias() -> None:
    """type_ must deserialise from the 'type' JSON key."""
    obj = DtcMonitor(**{"_ref": REF, "type": "TCP", "name": "mon1"})
    assert obj.type_ == "TCP"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "type" in dumped
    assert dumped["type"] == "TCP"


async def test_dtc_monitor_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc_monitor import DtcMonitorResource

    assert DtcMonitorResource._wapi_type == "dtc:monitor"
