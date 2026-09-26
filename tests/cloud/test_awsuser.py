# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AwsuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.cloud.models.awsuser import Awsuser
from tests.conftest import json_response

WAPI_TYPE = "awsuser"
REF = f"{WAPI_TYPE}/ZG5z:user1"


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


async def test_awsuser_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF, "name": "user1"}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.cloud.awsuser.list().all()
        assert len(records) == 1
        assert records[0].name == "user1"
        assert captured[0].url.params["_paging"] == "1"


async def test_awsuser_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "user1"})) as c:
        r = await c.cloud.awsuser.get(REF)
        assert r.name == "user1"
        assert r.ref == REF


async def test_awsuser_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "user1"}], "next_page_id": ""})
    ) as c:
        r = await c.cloud.awsuser.find_one(name="user1")
        assert r is not None
        assert r.name == "user1"


async def test_awsuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "user1"})

    async with _client(handler) as c:
        r = await c.cloud.awsuser.create(
            {"name": "user1", "access_key_id": "AKIAIOSFODNN7EXAMPLE"}
        )
        assert r.name == "user1"
        req = captured[0]
        assert req.method == "POST"
        assert '"user1"' in req.content.decode()


async def test_awsuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "user1"})

    async with _client(handler) as c:
        obj = Awsuser(**{"_ref": REF, "name": "user1", "uuid": "ro-uuid", "status": "ACTIVE"})
        await c.cloud.awsuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"user1"' in body


async def test_awsuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.cloud.awsuser.delete(REF)
        assert result == REF
