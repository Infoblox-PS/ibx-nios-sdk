# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AuthpolicyResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.authpolicy import Authpolicy
from tests.conftest import json_response

WAPI_TYPE = "authpolicy"
REF = f"{WAPI_TYPE}/ZG5z:policy"


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


async def test_authpolicy_list() -> None:
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
                        "auth_services": ["localuser:authservice/abc"],
                        "default_group": "admin-group",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.authpolicy.list().all()
        assert len(records) == 1
        assert records[0].default_group == "admin-group"
        assert captured[0].url.params["_paging"] == "1"


async def test_authpolicy_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "auth_services": ["localuser:authservice/abc"],
                "default_group": "admin-group",
            }
        )
    ) as c:
        r = await c.security.authpolicy.get(REF)
        assert r.default_group == "admin-group"
        assert r.auth_services == ["localuser:authservice/abc"]


async def test_authpolicy_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "auth_services": [],
                        "default_group": "admin-group",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.authpolicy.find_one(default_group="admin-group")
        assert r is not None
        assert r.default_group == "admin-group"


async def test_authpolicy_create() -> None:
    """authpolicy create - WapiResource.create is available (WAPI may reject for singleton)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "auth_services": [], "default_group": "admin-group"})

    async with _client(handler) as c:
        r = await c.security.authpolicy.create({"default_group": "admin-group"})
        assert r.default_group == "admin-group"
        req = captured[0]
        assert req.method == "POST"


async def test_authpolicy_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "default_group": "admin-group"})

    async with _client(handler) as c:
        obj = Authpolicy(
            **{
                "_ref": REF,
                "default_group": "admin-group",
                "auth_services": ["localuser:authservice/abc"],
                "uuid": "ro-uuid",
            }
        )
        await c.security.authpolicy.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"admin-group"' in body


async def test_authpolicy_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.authpolicy.delete(REF)
        assert result == REF
