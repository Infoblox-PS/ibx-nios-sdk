# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderGlobalResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.smartfolder.models.smartfolder_global import SmartfolderGlobal
from tests.conftest import json_response

WAPI_TYPE = "smartfolder:global"
REF = f"{WAPI_TYPE}/ZG5z:folder1"


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


async def test_smartfolder_global_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "folder1", "comment": "global folder"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.smartfolder.global_.list().all()
        assert len(records) == 1
        assert records[0].name == "folder1"
        assert captured[0].url.params["_paging"] == "1"


async def test_smartfolder_global_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "folder1"})) as c:
        r = await c.smartfolder.global_.get(REF)
        assert r.name == "folder1"
        assert r.ref == REF


async def test_smartfolder_global_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "folder1"}], "next_page_id": ""})
    ) as c:
        r = await c.smartfolder.global_.find_one(name="folder1")
        assert r is not None
        assert r.name == "folder1"


async def test_smartfolder_global_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "folder1"})

    async with _client(handler) as c:
        r = await c.smartfolder.global_.create({"name": "folder1", "comment": "my folder"})
        assert r.name == "folder1"
        req = captured[0]
        assert req.method == "POST"
        assert '"folder1"' in req.content.decode()


async def test_smartfolder_global_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "folder1"})

    async with _client(handler) as c:
        obj = SmartfolderGlobal(**{"_ref": REF, "name": "folder1", "uuid": "ro-uuid"})
        await c.smartfolder.global_.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"folder1"' in body


async def test_smartfolder_global_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.smartfolder.global_.delete(REF)
        assert result == REF
