# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdminuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.adminuser import Adminuser
from tests.conftest import json_response

WAPI_TYPE = "adminuser"
REF = f"{WAPI_TYPE}/ZG5z:jdoe"


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


async def test_adminuser_list() -> None:
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
                        "name": "jdoe",
                        "comment": "test user",
                        "admin_groups": ["admin-group-1"],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.adminuser.list().all()
        assert len(records) == 1
        assert records[0].name == "jdoe"
        assert records[0].admin_groups == ["admin-group-1"]
        assert captured[0].url.params["_paging"] == "1"


async def test_adminuser_get() -> None:
    async with _client(
        _session_handler(
            {"_ref": REF, "name": "jdoe", "comment": "test", "admin_groups": ["admins"]}
        )
    ) as c:
        r = await c.security.adminuser.get(REF)
        assert r.name == "jdoe"
        assert r.admin_groups == ["admins"]


async def test_adminuser_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "jdoe", "comment": "", "admin_groups": []}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.adminuser.find_one(name="jdoe")
        assert r is not None
        assert r.name == "jdoe"


async def test_adminuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": REF, "name": "jdoe", "comment": "created", "admin_groups": ["admins"]}
        )

    async with _client(handler) as c:
        r = await c.security.adminuser.create(
            {"name": "jdoe", "comment": "created", "admin_groups": ["admins"]}
        )
        assert r.name == "jdoe"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"jdoe"' in body


async def test_adminuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "jdoe", "comment": "updated"})

    async with _client(handler) as c:
        obj = Adminuser(
            **{
                "_ref": REF,
                "name": "jdoe",
                "comment": "updated",
                "status": "ACTIVE",
                "uuid": "ro-uuid",
            }
        )
        await c.security.adminuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"jdoe"' in body


async def test_adminuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.adminuser.delete(REF)
        assert result == REF
