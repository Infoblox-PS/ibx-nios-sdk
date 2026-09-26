# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LocaluserAuthserviceResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.localuser_authservice import LocaluserAuthservice
from tests.conftest import json_response

WAPI_TYPE = "localuser:authservice"
REF = f"{WAPI_TYPE}/ZG5z:localuser"


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


async def test_localuser_authservice_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "name": "Local User Auth Service", "comment": "built-in"}
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.localuser_authservice.list().all()
        assert len(records) == 1
        assert records[0].name == "Local User Auth Service"
        assert captured[0].url.params["_paging"] == "1"


async def test_localuser_authservice_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "Local User Auth Service",
                "comment": "built-in",
                "disabled": False,
            }
        )
    ) as c:
        r = await c.security.localuser_authservice.get(REF)
        assert r.name == "Local User Auth Service"
        assert r.disabled is False


async def test_localuser_authservice_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {"_ref": REF, "name": "Local User Auth Service", "comment": "built-in"}
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.localuser_authservice.find_one(name="Local User Auth Service")
        assert r is not None
        assert r.name == "Local User Auth Service"


async def test_localuser_authservice_create() -> None:
    """localuser:authservice create - WapiResource.create available (all fields readOnly)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "Local User Auth Service"})

    async with _client(handler) as c:
        r = await c.security.localuser_authservice.create({})
        assert r.ref == REF
        req = captured[0]
        assert req.method == "POST"


async def test_localuser_authservice_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = LocaluserAuthservice(
            **{
                "_ref": REF,
                "name": "Local User Auth Service",
                "comment": "built-in",
                "disabled": False,
            }
        )
        await c.security.localuser_authservice.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"comment"' not in body, "comment is readonly - must be stripped"
        assert '"disabled"' not in body, "disabled is readonly - must be stripped"


async def test_localuser_authservice_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.localuser_authservice.delete(REF)
        assert result == REF
