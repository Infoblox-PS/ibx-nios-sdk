# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordSrvResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_record_srv import DtcRecordSrv
from tests.conftest import json_response

WAPI_TYPE = "dtc:record:srv"
REF = f"{WAPI_TYPE}/ZG5z:recsrv1"


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


async def test_dtc_record_srv_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "_sip._tcp", "target": "sip.example.com"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.record_srv.list().all()
        assert len(records) == 1
        assert records[0].name == "_sip._tcp"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_record_srv_get() -> None:
    async with _client(
        _session_handler(
            {"_ref": REF, "name": "_sip._tcp", "target": "sip.example.com", "port": 5060}
        )
    ) as c:
        r = await c.dtc.record_srv.get(REF)
        assert r.name == "_sip._tcp"
        assert r.port == 5060


async def test_dtc_record_srv_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "_sip._tcp"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.record_srv.find_one()
        assert r is not None
        assert r.name == "_sip._tcp"


async def test_dtc_record_srv_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "_sip._tcp"})

    async with _client(handler) as c:
        r = await c.dtc.record_srv.create(
            {
                "name": "_sip._tcp",
                "target": "sip.example.com",
                "port": 5060,
                "priority": 10,
                "weight": 20,
            }
        )
        assert r.name == "_sip._tcp"
        assert captured[0].method == "POST"


async def test_dtc_record_srv_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DtcRecordSrv(**{"_ref": REF, "name": "_sip._tcp", "uuid": "ro-uuid"})
        await c.dtc.record_srv.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert "_sip._tcp" in body


async def test_dtc_record_srv_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.record_srv.delete(REF)
        assert result == REF
