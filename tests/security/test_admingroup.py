# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdmingroupResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.admingroup import Admingroup
from tests.conftest import json_response

WAPI_TYPE = "admingroup"
REF = f"{WAPI_TYPE}/ZG5z:admins"


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


async def test_admingroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "name": "admin-group-1", "comment": "test group"},
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.admingroup.list().all()
        assert len(records) == 1
        assert records[0].name == "admin-group-1"
        params = captured[0].url.params
        assert params["_paging"] == "1"


async def test_admingroup_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "admin-group-1", "comment": "test"})
    ) as c:
        r = await c.security.admingroup.get(REF)
        assert r.name == "admin-group-1"
        assert r.ref == REF


async def test_admingroup_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "admin-group-1", "comment": ""}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.admingroup.find_one(name="admin-group-1")
        assert r is not None
        assert r.name == "admin-group-1"


async def test_admingroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "admin-group-1", "comment": "created"})

    async with _client(handler) as c:
        r = await c.security.admingroup.create({"name": "admin-group-1", "comment": "created"})
        assert r.name == "admin-group-1"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"
        body = req.content.decode()
        assert '"admin-group-1"' in body


async def test_admingroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "admin-group-1", "comment": "updated"})

    async with _client(handler) as c:
        obj = Admingroup(
            **{"_ref": REF, "name": "admin-group-1", "comment": "updated", "uuid": "ro-uuid"}
        )
        await c.security.admingroup.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"admin-group-1"' in body


async def test_admingroup_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.admingroup.delete(REF)
        assert result == REF
