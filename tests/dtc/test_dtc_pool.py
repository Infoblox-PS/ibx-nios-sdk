# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcPoolResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_pool import DtcPool
from tests.conftest import json_response

WAPI_TYPE = "dtc:pool"
REF = f"{WAPI_TYPE}/ZG5z:pool1"


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


async def test_dtc_pool_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "pool1", "comment": "test"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.pool.list().all()
        assert len(records) == 1
        assert records[0].name == "pool1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_pool_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "pool1", "availability": "ALL"})
    ) as c:
        r = await c.dtc.pool.get(REF)
        assert r.name == "pool1"
        assert r.availability == "ALL"


async def test_dtc_pool_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "pool1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.pool.find_one(name="pool1")
        assert r is not None
        assert r.name == "pool1"


async def test_dtc_pool_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "pool1"})

    async with _client(handler) as c:
        r = await c.dtc.pool.create({"name": "pool1", "lb_preferred_method": "ROUND_ROBIN"})
        assert r.name == "pool1"
        req = captured[0]
        assert req.method == "POST"
        assert '"pool1"' in req.content.decode()


async def test_dtc_pool_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "pool1"})

    async with _client(handler) as c:
        obj = DtcPool(**{"_ref": REF, "name": "pool1", "uuid": "ro-uuid"})
        await c.dtc.pool.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"pool1"' in body


async def test_dtc_pool_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.pool.delete(REF)
        assert result == REF
