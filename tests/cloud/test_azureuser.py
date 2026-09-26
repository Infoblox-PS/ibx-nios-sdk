# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AzureuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.cloud.models.azureuser import Azureuser
from tests.conftest import json_response

WAPI_TYPE = "azureuser"
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


async def test_azureuser_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF, "name": "azuser1"}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.cloud.azureuser.list().all()
        assert len(records) == 1
        assert records[0].name == "azuser1"
        assert captured[0].url.params["_paging"] == "1"


async def test_azureuser_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "azuser1"})) as c:
        r = await c.cloud.azureuser.get(REF)
        assert r.name == "azuser1"
        assert r.ref == REF


async def test_azureuser_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "azuser1"}], "next_page_id": ""})
    ) as c:
        r = await c.cloud.azureuser.find_one(name="azuser1")
        assert r is not None
        assert r.name == "azuser1"


async def test_azureuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "azuser1"})

    async with _client(handler) as c:
        r = await c.cloud.azureuser.create({"name": "azuser1", "client_id": "client-abc"})
        assert r.name == "azuser1"
        req = captured[0]
        assert req.method == "POST"
        assert '"azuser1"' in req.content.decode()


async def test_azureuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "azuser1"})

    async with _client(handler) as c:
        obj = Azureuser(**{"_ref": REF, "name": "azuser1", "uuid": "ro-uuid", "status": "ACTIVE"})
        await c.cloud.azureuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"azuser1"' in body


async def test_azureuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.cloud.azureuser.delete(REF)
        assert result == REF
