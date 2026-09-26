# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdminroleResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.adminrole import Adminrole
from tests.conftest import json_response

WAPI_TYPE = "adminrole"
REF = f"{WAPI_TYPE}/ZG5z:role1"


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


async def test_adminrole_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "role1", "comment": "test role"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.adminrole.list().all()
        assert len(records) == 1
        assert records[0].name == "role1"
        assert captured[0].url.params["_paging"] == "1"


async def test_adminrole_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "role1", "comment": "test"})) as c:
        r = await c.security.adminrole.get(REF)
        assert r.name == "role1"
        assert r.ref == REF


async def test_adminrole_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "name": "role1", "comment": ""}], "next_page_id": ""}
        )
    ) as c:
        r = await c.security.adminrole.find_one(name="role1")
        assert r is not None
        assert r.name == "role1"


async def test_adminrole_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "role1", "comment": "created"})

    async with _client(handler) as c:
        r = await c.security.adminrole.create({"name": "role1", "comment": "created"})
        assert r.name == "role1"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"role1"' in body


async def test_adminrole_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "role1", "comment": "updated"})

    async with _client(handler) as c:
        obj = Adminrole(**{"_ref": REF, "name": "role1", "comment": "updated", "uuid": "ro-uuid"})
        await c.security.adminrole.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"role1"' in body


async def test_adminrole_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.adminrole.delete(REF)
        assert result == REF
