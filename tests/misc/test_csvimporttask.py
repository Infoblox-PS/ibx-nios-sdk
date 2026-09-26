# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CsvimporttaskResource - list, get, find_one, update_strips_readonly, list_empty, paging."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.csvimporttask import Csvimporttask
from tests.conftest import json_response

WAPI_TYPE = "csvimporttask"
REF = f"{WAPI_TYPE}/ZG5z:task1"


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


async def test_csvimporttask_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": REF,
                        "file_name": "import.csv",
                        "status": "COMPLETED",
                        "action": "MERGE",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.csvimporttask.list().all()
        assert len(records) == 1
        assert records[0].file_name == "import.csv"
        assert records[0].status == "COMPLETED"
        assert captured[0].url.params["_paging"] == "1"


async def test_csvimporttask_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "file_name": "import.csv", "status": "COMPLETED"})
    ) as c:
        r = await c.misc.csvimporttask.get(REF)
        assert r.file_name == "import.csv"
        assert r.ref == REF


async def test_csvimporttask_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "file_name": "import.csv"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.misc.csvimporttask.find_one(file_name="import.csv")
        assert r is not None
        assert r.file_name == "import.csv"


async def test_csvimporttask_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "action": "MERGE"})

    async with _client(handler) as c:
        obj = Csvimporttask(
            **{"_ref": REF, "action": "MERGE", "status": "COMPLETED", "uuid": "ro"}
        )
        await c.misc.csvimporttask.update(REF, obj)
        body = captured[0].content.decode()
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"MERGE"' in body


async def test_csvimporttask_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.csvimporttask.list().all()
        assert records == []


async def test_csvimporttask_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.csvimporttask.list(max_results=25).all()
        assert captured[0].url.params["_max_results"] == "25"
        assert captured[0].url.params["_return_as_object"] == "1"
