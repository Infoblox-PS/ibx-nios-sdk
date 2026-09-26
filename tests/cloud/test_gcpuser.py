# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GcpuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.cloud.models.gcpuser import Gcpuser
from tests.conftest import json_response

WAPI_TYPE = "gcpuser"
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


async def test_gcpuser_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "user_name": "gcpuser1"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.cloud.gcpuser.list().all()
        assert len(records) == 1
        assert records[0].user_name == "gcpuser1"
        assert captured[0].url.params["_paging"] == "1"


async def test_gcpuser_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "user_name": "gcpuser1", "type": "service_account"})
    ) as c:
        r = await c.cloud.gcpuser.get(REF)
        assert r.user_name == "gcpuser1"
        assert r.type_ == "service_account"
        assert r.ref == REF


async def test_gcpuser_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "user_name": "gcpuser1"}], "next_page_id": ""})
    ) as c:
        r = await c.cloud.gcpuser.find_one(user_name="gcpuser1")
        assert r is not None
        assert r.user_name == "gcpuser1"


async def test_gcpuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "user_name": "gcpuser1"})

    async with _client(handler) as c:
        r = await c.cloud.gcpuser.create({"user_name": "gcpuser1", "project_id": "my-proj"})
        assert r.user_name == "gcpuser1"
        req = captured[0]
        assert req.method == "POST"
        assert '"gcpuser1"' in req.content.decode()


async def test_gcpuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "user_name": "gcpuser1"})

    async with _client(handler) as c:
        obj = Gcpuser(
            **{"_ref": REF, "user_name": "gcpuser1", "uuid": "ro-uuid", "status": "ACTIVE"}
        )
        await c.cloud.gcpuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"gcpuser1"' in body


async def test_gcpuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.cloud.gcpuser.delete(REF)
        assert result == REF
