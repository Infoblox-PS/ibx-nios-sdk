# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordCnameResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_record_cname import DtcRecordCname
from tests.conftest import json_response

WAPI_TYPE = "dtc:record:cname"
REF = f"{WAPI_TYPE}/ZG5z:reccname1"


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


async def test_dtc_record_cname_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "canonical": "foo.example.com", "dtc_server": "srv1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.record_cname.list().all()
        assert len(records) == 1
        assert records[0].canonical == "foo.example.com"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_record_cname_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "canonical": "foo.example.com", "dtc_server": "srv1"})
    ) as c:
        r = await c.dtc.record_cname.get(REF)
        assert r.canonical == "foo.example.com"


async def test_dtc_record_cname_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "canonical": "foo.example.com"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.dtc.record_cname.find_one()
        assert r is not None
        assert r.canonical == "foo.example.com"


async def test_dtc_record_cname_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "canonical": "foo.example.com"})

    async with _client(handler) as c:
        r = await c.dtc.record_cname.create({"canonical": "foo.example.com", "dtc_server": "srv1"})
        assert r.canonical == "foo.example.com"
        assert captured[0].method == "POST"


async def test_dtc_record_cname_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DtcRecordCname(
            **{
                "_ref": REF,
                "canonical": "foo.example.com",
                "dns_canonical": "ro-dns",
                "uuid": "ro-uuid",
            }
        )
        await c.dtc.record_cname.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"dns_canonical"' not in body
        assert "foo.example.com" in body


async def test_dtc_record_cname_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.record_cname.delete(REF)
        assert result == REF
