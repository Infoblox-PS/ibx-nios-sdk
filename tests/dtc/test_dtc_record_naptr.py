# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordNaptrResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_record_naptr import DtcRecordNaptr
from tests.conftest import json_response

WAPI_TYPE = "dtc:record:naptr"
REF = f"{WAPI_TYPE}/ZG5z:recnaptr1"


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


async def test_dtc_record_naptr_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "services": "SIP+D2U", "dtc_server": "srv1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.record_naptr.list().all()
        assert len(records) == 1
        assert records[0].services == "SIP+D2U"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_record_naptr_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "services": "SIP+D2U",
                "order": 10,
                "preference": 20,
                "dtc_server": "srv1",
            }
        )
    ) as c:
        r = await c.dtc.record_naptr.get(REF)
        assert r.services == "SIP+D2U"
        assert r.order == 10


async def test_dtc_record_naptr_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "services": "SIP+D2U"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.record_naptr.find_one()
        assert r is not None
        assert r.services == "SIP+D2U"


async def test_dtc_record_naptr_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "services": "SIP+D2U"})

    async with _client(handler) as c:
        r = await c.dtc.record_naptr.create(
            {"services": "SIP+D2U", "order": 10, "preference": 20, "dtc_server": "srv1"}
        )
        assert r.services == "SIP+D2U"
        assert captured[0].method == "POST"


async def test_dtc_record_naptr_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DtcRecordNaptr(**{"_ref": REF, "services": "SIP+D2U", "uuid": "ro-uuid"})
        await c.dtc.record_naptr.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert "SIP+D2U" in body


async def test_dtc_record_naptr_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.record_naptr.delete(REF)
        assert result == REF
