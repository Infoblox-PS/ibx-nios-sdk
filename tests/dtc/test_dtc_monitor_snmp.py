# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorSnmpResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_monitor_snmp import DtcMonitorSnmp
from tests.conftest import json_response

WAPI_TYPE = "dtc:monitor:snmp"
REF = f"{WAPI_TYPE}/ZG5z:snmp1"


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


async def test_dtc_monitor_snmp_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "snmp1", "community": "public"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.monitor_snmp.list().all()
        assert len(records) == 1
        assert records[0].name == "snmp1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_monitor_snmp_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "snmp1", "community": "public", "version": "V2C"})
    ) as c:
        r = await c.dtc.monitor_snmp.get(REF)
        assert r.name == "snmp1"
        assert r.version == "V2C"


async def test_dtc_monitor_snmp_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "snmp1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.monitor_snmp.find_one(name="snmp1")
        assert r is not None
        assert r.name == "snmp1"


async def test_dtc_monitor_snmp_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "snmp1"})

    async with _client(handler) as c:
        r = await c.dtc.monitor_snmp.create(
            {"name": "snmp1", "community": "public", "version": "V2C"}
        )
        assert r.name == "snmp1"
        assert captured[0].method == "POST"


async def test_dtc_monitor_snmp_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "snmp1"})

    async with _client(handler) as c:
        obj = DtcMonitorSnmp(
            **{"_ref": REF, "name": "snmp1", "uuid": "ro-uuid", "oids": [{"oid": "1.3.6.1"}]}
        )
        await c.dtc.monitor_snmp.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"snmp1"' in body


async def test_dtc_monitor_snmp_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.monitor_snmp.delete(REF)
        assert result == REF
