# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""PermissionResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.permission import Permission
from tests.conftest import json_response

WAPI_TYPE = "permission"
REF = f"{WAPI_TYPE}/ZG5z:perm1"


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


async def test_permission_list() -> None:
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
                        "permission": "WRITE",
                        "resource_type": "ZONE",
                        "group": "admin-group-1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.permission.list().all()
        assert len(records) == 1
        assert records[0].permission == "WRITE"
        assert records[0].resource_type == "ZONE"
        assert captured[0].url.params["_paging"] == "1"


async def test_permission_get() -> None:
    async with _client(
        _session_handler(
            {"_ref": REF, "permission": "READ", "resource_type": "ZONE", "group": "admins"}
        )
    ) as c:
        r = await c.security.permission.get(REF)
        assert r.permission == "READ"


async def test_permission_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {"_ref": REF, "permission": "WRITE", "resource_type": "ZONE", "group": "g"}
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.permission.find_one(resource_type="ZONE")
        assert r is not None
        assert r.permission == "WRITE"


async def test_permission_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": REF, "permission": "WRITE", "resource_type": "ZONE", "group": "admins"}
        )

    async with _client(handler) as c:
        r = await c.security.permission.create(
            {"permission": "WRITE", "resource_type": "ZONE", "group": "admins"}
        )
        assert r.permission == "WRITE"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"WRITE"' in body


async def test_permission_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "permission": "READ", "resource_type": "ZONE"})

    async with _client(handler) as c:
        obj = Permission(
            **{"_ref": REF, "permission": "READ", "resource_type": "ZONE", "uuid": "ro-uuid"}
        )
        await c.security.permission.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"READ"' in body


async def test_permission_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.permission.delete(REF)
        assert result == REF
