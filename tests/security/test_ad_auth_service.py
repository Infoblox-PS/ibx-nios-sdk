# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdAuthServiceResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.ad_auth_service import AdAuthService
from tests.conftest import json_response

WAPI_TYPE = "ad_auth_service"
REF = f"{WAPI_TYPE}/ZG5z:ad1"


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


async def test_ad_auth_service_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "ad-svc", "comment": "AD auth"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.ad_auth_service.list().all()
        assert len(records) == 1
        assert records[0].name == "ad-svc"
        assert captured[0].url.params["_paging"] == "1"


async def test_ad_auth_service_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "ad-svc",
                "comment": "test",
                "ad_domain": "corp.example.com",
            }
        )
    ) as c:
        r = await c.security.ad_auth_service.get(REF)
        assert r.name == "ad-svc"
        assert r.ad_domain == "corp.example.com"


async def test_ad_auth_service_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "ad-svc", "comment": ""}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.ad_auth_service.find_one(name="ad-svc")
        assert r is not None
        assert r.name == "ad-svc"


async def test_ad_auth_service_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": REF, "name": "ad-svc", "comment": "created", "ad_domain": "corp.example.com"}
        )

    async with _client(handler) as c:
        r = await c.security.ad_auth_service.create(
            {"name": "ad-svc", "ad_domain": "corp.example.com"}
        )
        assert r.name == "ad-svc"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"ad-svc"' in body


async def test_ad_auth_service_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "ad-svc", "comment": "updated"})

    async with _client(handler) as c:
        obj = AdAuthService(
            **{"_ref": REF, "name": "ad-svc", "comment": "updated", "uuid": "ro-uuid"}
        )
        await c.security.ad_auth_service.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"ad-svc"' in body


async def test_ad_auth_service_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.ad_auth_service.delete(REF)
        assert result == REF
