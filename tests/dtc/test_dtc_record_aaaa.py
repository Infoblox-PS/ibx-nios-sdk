# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordAaaaResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_record_aaaa import DtcRecordAaaa
from tests.conftest import json_response

WAPI_TYPE = "dtc:record:aaaa"
REF = f"{WAPI_TYPE}/ZG5z:recaaaa1"


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


async def test_dtc_record_aaaa_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "ipv6addr": "2001:db8::1", "dtc_server": "srv1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.record_aaaa.list().all()
        assert len(records) == 1
        assert records[0].ipv6addr == "2001:db8::1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_record_aaaa_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "ipv6addr": "2001:db8::1", "dtc_server": "srv1"})
    ) as c:
        r = await c.dtc.record_aaaa.get(REF)
        assert r.ipv6addr == "2001:db8::1"


async def test_dtc_record_aaaa_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "ipv6addr": "2001:db8::1"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.dtc.record_aaaa.find_one()
        assert r is not None
        assert r.ipv6addr == "2001:db8::1"


async def test_dtc_record_aaaa_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "ipv6addr": "2001:db8::1"})

    async with _client(handler) as c:
        r = await c.dtc.record_aaaa.create({"ipv6addr": "2001:db8::1", "dtc_server": "srv1"})
        assert r.ipv6addr == "2001:db8::1"
        assert captured[0].method == "POST"


async def test_dtc_record_aaaa_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DtcRecordAaaa(**{"_ref": REF, "ipv6addr": "2001:db8::1", "uuid": "ro-uuid"})
        await c.dtc.record_aaaa.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert "2001:db8::1" in body


async def test_dtc_record_aaaa_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.record_aaaa.delete(REF)
        assert result == REF
