# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DeletedObjectsResource - list, get, find_one (read-only)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "deleted_objects"
REF = f"{WAPI_TYPE}/ZG5z:del1"


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


async def test_deleted_objects_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "object_type": "record:a"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.deleted_objects.list().all()
        assert len(records) == 1
        assert records[0].object_type == "record:a"
        assert captured[0].url.params["_paging"] == "1"


async def test_deleted_objects_get() -> None:
    async with _client(_session_handler({"_ref": REF, "object_type": "record:a"})) as c:
        r = await c.misc.deleted_objects.get(REF)
        assert r.object_type == "record:a"
        assert r.ref == REF


async def test_deleted_objects_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "object_type": "record:a"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.misc.deleted_objects.find_one(object_type="record:a")
        assert r is not None
        assert r.object_type == "record:a"


async def test_deleted_objects_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.deleted_objects.list().all()
        assert records == []


async def test_deleted_objects_find_one_none() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        r = await c.misc.deleted_objects.find_one(object_type="NONE")
        assert r is None


async def test_deleted_objects_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.deleted_objects.list(max_results=200).all()
        assert captured[0].url.params["_max_results"] == "200"
