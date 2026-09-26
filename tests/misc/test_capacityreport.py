# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CapacityreportResource - list, get, find_one (read-only)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "capacityreport"
REF = f"{WAPI_TYPE}/ZG5z:cr1"


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


async def test_capacityreport_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "gm", "percent_used": 42, "total_objects": 1000}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.capacityreport.list().all()
        assert len(records) == 1
        assert records[0].name == "gm"
        assert records[0].percent_used == 42
        assert captured[0].url.params["_paging"] == "1"


async def test_capacityreport_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "gm", "percent_used": 42, "total_objects": 1000})
    ) as c:
        r = await c.misc.capacityreport.get(REF)
        assert r.name == "gm"
        assert r.ref == REF


async def test_capacityreport_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "gm"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.capacityreport.find_one(name="gm")
        assert r is not None
        assert r.name == "gm"


async def test_capacityreport_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.capacityreport.list().all()
        assert records == []


async def test_capacityreport_find_one_none() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        r = await c.misc.capacityreport.find_one(name="NONE")
        assert r is None


async def test_capacityreport_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.capacityreport.list(max_results=10).all()
        assert captured[0].url.params["_max_results"] == "10"
        assert captured[0].url.params["_return_as_object"] == "1"
