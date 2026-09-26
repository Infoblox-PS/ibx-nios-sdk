# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MssuperscopeResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.microsoftserver.models.mssuperscope import Mssuperscope
from tests.conftest import json_response

WAPI_TYPE = "mssuperscope"
REF = f"{WAPI_TYPE}/ZG5z:ss1"


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


async def test_mssuperscope_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "ss1", "network_view": "default"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.microsoftserver.mssuperscope.list().all()
        assert len(records) == 1
        assert records[0].name == "ss1"
        assert records[0].network_view == "default"
        assert captured[0].url.params["_paging"] == "1"


async def test_mssuperscope_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "ss1", "comment": "corp superscope"})
    ) as c:
        r = await c.microsoftserver.mssuperscope.get(REF)
        assert r.name == "ss1"
        assert r.comment == "corp superscope"


async def test_mssuperscope_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "ss1"}], "next_page_id": ""})
    ) as c:
        r = await c.microsoftserver.mssuperscope.find_one(name="ss1")
        assert r is not None
        assert r.name == "ss1"


async def test_mssuperscope_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "ss1"})

    async with _client(handler) as c:
        r = await c.microsoftserver.mssuperscope.create({"name": "ss1", "network_view": "default"})
        assert r.name == "ss1"
        req = captured[0]
        assert req.method == "POST"
        assert '"ss1"' in req.content.decode()


async def test_mssuperscope_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = Mssuperscope(
            **{
                "_ref": REF,
                "name": "ss1",
                "comment": "updated",
                "dhcp_utilization": 75,
                "total_hosts": 1000,
                "dynamic_hosts": 500,
                "static_hosts": 500,
                "uuid": "ro-uuid",
                "high_water_mark": 80,
            }
        )
        await c.microsoftserver.mssuperscope.update(REF, obj)
        body = captured[0].content.decode()
        assert '"dhcp_utilization"' not in body, "dhcp_utilization is readonly - must be stripped"
        assert '"total_hosts"' not in body, "total_hosts is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"updated"' in body
        assert '"high_water_mark"' not in body, "high_water_mark is readonly per live schema"


async def test_mssuperscope_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.microsoftserver.mssuperscope.delete(REF)
        assert result == REF
