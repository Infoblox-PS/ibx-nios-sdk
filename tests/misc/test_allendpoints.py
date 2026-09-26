# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AllendpointsResource - list, get, find_one (read-only aggregate)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "allendpoints"
REF = f"{WAPI_TYPE}/ZG5z:ep1"


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


async def test_allendpoints_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "type": "DXL", "address": "10.0.0.1", "comment": "ep1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.allendpoints.list().all()
        assert len(records) == 1
        assert records[0].type == "DXL"
        assert records[0].address == "10.0.0.1"
        assert captured[0].url.params["_paging"] == "1"


async def test_allendpoints_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "type": "DXL", "address": "10.0.0.1", "comment": "ep1"})
    ) as c:
        r = await c.misc.allendpoints.get(REF)
        assert r.type == "DXL"
        assert r.ref == REF


async def test_allendpoints_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "type": "DXL", "comment": "ep1"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.misc.allendpoints.find_one(type="DXL")
        assert r is not None
        assert r.type == "DXL"


async def test_allendpoints_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.allendpoints.list().all()
        assert records == []


async def test_allendpoints_find_one_none() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        r = await c.misc.allendpoints.find_one(type="NONEXISTENT")
        assert r is None


async def test_allendpoints_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.allendpoints.list(max_results=50).all()
        assert captured[0].url.params["_max_results"] == "50"
        assert captured[0].url.params["_return_as_object"] == "1"
