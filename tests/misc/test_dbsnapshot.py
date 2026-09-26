# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DbsnapshotResource - list, get, find_one, update_strips_readonly, list_empty, paging."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.dbsnapshot import Dbsnapshot
from tests.conftest import json_response

WAPI_TYPE = "dbsnapshot"
REF = f"{WAPI_TYPE}/ZG5z:snap1"


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


async def test_dbsnapshot_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "comment": "backup", "timestamp": 1700000000}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.dbsnapshot.list().all()
        assert len(records) == 1
        assert records[0].comment == "backup"
        assert captured[0].url.params["_paging"] == "1"


async def test_dbsnapshot_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "comment": "backup", "timestamp": 1700000000})
    ) as c:
        r = await c.misc.dbsnapshot.get(REF)
        assert r.comment == "backup"
        assert r.ref == REF


async def test_dbsnapshot_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "comment": "backup"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.dbsnapshot.find_one(comment="backup")
        assert r is not None
        assert r.comment == "backup"


async def test_dbsnapshot_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = Dbsnapshot(**{"_ref": REF, "comment": "backup", "timestamp": 123, "uuid": "ro"})
        await c.misc.dbsnapshot.update(REF, obj)
        body = captured[0].content.decode()
        assert '"comment"' not in body, "comment is readonly - must be stripped"
        assert '"timestamp"' not in body, "timestamp is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"


async def test_dbsnapshot_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.dbsnapshot.list().all()
        assert records == []


async def test_dbsnapshot_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.dbsnapshot.list(max_results=5).all()
        assert captured[0].url.params["_max_results"] == "5"
