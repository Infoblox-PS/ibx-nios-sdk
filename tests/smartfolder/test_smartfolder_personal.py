# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderPersonalResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.smartfolder.models.smartfolder_personal import SmartfolderPersonal
from tests.conftest import json_response

WAPI_TYPE = "smartfolder:personal"
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


async def test_smartfolder_personal_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "myfolder", "comment": "personal folder"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.smartfolder.personal.list().all()
        assert len(records) == 1
        assert records[0].name == "myfolder"
        assert captured[0].url.params["_paging"] == "1"


async def test_smartfolder_personal_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "myfolder", "is_shortcut": False})
    ) as c:
        r = await c.smartfolder.personal.get(REF)
        assert r.name == "myfolder"
        assert r.is_shortcut is False
        assert r.ref == REF


async def test_smartfolder_personal_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "myfolder"}], "next_page_id": ""})
    ) as c:
        r = await c.smartfolder.personal.find_one(name="myfolder")
        assert r is not None
        assert r.name == "myfolder"


async def test_smartfolder_personal_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "myfolder"})

    async with _client(handler) as c:
        r = await c.smartfolder.personal.create({"name": "myfolder", "comment": "mine"})
        assert r.name == "myfolder"
        req = captured[0]
        assert req.method == "POST"
        assert '"myfolder"' in req.content.decode()


async def test_smartfolder_personal_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "myfolder"})

    async with _client(handler) as c:
        obj = SmartfolderPersonal(**{"_ref": REF, "name": "myfolder", "is_shortcut": True})
        await c.smartfolder.personal.update(REF, obj)
        body = captured[0].content.decode()
        assert '"is_shortcut"' not in body, "is_shortcut is readonly - must be stripped"
        assert '"myfolder"' in body


async def test_smartfolder_personal_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.smartfolder.personal.delete(REF)
        assert result == REF
