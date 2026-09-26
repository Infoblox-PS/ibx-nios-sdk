# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcServerResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_server import DtcServer
from tests.conftest import json_response

WAPI_TYPE = "dtc:server"
REF = f"{WAPI_TYPE}/ZG5z:server1"


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


async def test_dtc_server_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "srv1", "comment": "test"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.server.list().all()
        assert len(records) == 1
        assert records[0].name == "srv1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_server_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "srv1", "comment": "test"})) as c:
        r = await c.dtc.server.get(REF)
        assert r.name == "srv1"
        assert r.ref == REF


async def test_dtc_server_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "name": "srv1", "comment": ""}], "next_page_id": ""}
        )
    ) as c:
        r = await c.dtc.server.find_one(name="srv1")
        assert r is not None
        assert r.name == "srv1"


async def test_dtc_server_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "srv1", "comment": "created"})

    async with _client(handler) as c:
        r = await c.dtc.server.create({"name": "srv1", "host": "1.2.3.4"})
        assert r.name == "srv1"
        req = captured[0]
        assert req.method == "POST"
        assert '"srv1"' in req.content.decode()


async def test_dtc_server_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "srv1"})

    async with _client(handler) as c:
        obj = DtcServer(**{"_ref": REF, "name": "srv1", "uuid": "ro-uuid"})
        await c.dtc.server.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"srv1"' in body


async def test_dtc_server_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.server.delete(REF)
        assert result == REF
