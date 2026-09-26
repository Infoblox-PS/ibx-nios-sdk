# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""UserprofileResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.userprofile import Userprofile
from tests.conftest import json_response

WAPI_TYPE = "userprofile"
REF = f"{WAPI_TYPE}/ZG5z:admin"


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


async def test_userprofile_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "admin", "admin_group": "admins"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.userprofile.list().all()
        assert len(records) == 1
        assert records[0].name == "admin"
        assert captured[0].url.params["_paging"] == "1"


async def test_userprofile_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "admin", "admin_group": "admins"})
    ) as c:
        r = await c.security.userprofile.get(REF)
        assert r.name == "admin"
        assert r.admin_group == "admins"


async def test_userprofile_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "admin", "admin_group": "admins"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.userprofile.find_one(name="admin")
        assert r is not None
        assert r.name == "admin"


async def test_userprofile_create() -> None:
    """userprofile create - WapiResource.create is available (WAPI may reject it)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "admin", "admin_group": "admins"})

    async with _client(handler) as c:
        r = await c.security.userprofile.create({"email": "admin@example.com"})
        assert r.name == "admin"
        req = captured[0]
        assert req.method == "POST"


async def test_userprofile_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "admin"})

    async with _client(handler) as c:
        obj = Userprofile(
            **{
                "_ref": REF,
                "name": "admin",
                "admin_group": "admins",
                "days_to_expire": 30,
                "email": "admin@example.com",
            }
        )
        await c.security.userprofile.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"admin_group"' not in body, "admin_group is readonly - must be stripped"
        assert '"days_to_expire"' not in body, "days_to_expire is readonly - must be stripped"
        assert '"email"' in body


async def test_userprofile_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.userprofile.delete(REF)
        assert result == REF
