# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.networkuser import Networkuser
from tests.conftest import json_response

WAPI_TYPE = "networkuser"
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


async def test_networkuser_list() -> None:
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
                        "address": "10.1.1.1",
                        "user_status": "ACTIVE",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.networkuser.list().all()
        assert len(records) == 1
        assert records[0].name == "jdoe"
        assert records[0].user_status == "ACTIVE"
        assert captured[0].url.params["_paging"] == "1"


async def test_networkuser_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "jdoe",
                "address": "10.1.1.1",
                "user_status": "ACTIVE",
                "domainname": "corp.example.com",
            }
        )
    ) as c:
        r = await c.security.networkuser.get(REF)
        assert r.name == "jdoe"
        assert r.address == "10.1.1.1"
        assert r.user_status == "ACTIVE"


async def test_networkuser_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "jdoe", "address": "10.1.1.1"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.networkuser.find_one(name="jdoe")
        assert r is not None
        assert r.name == "jdoe"


async def test_networkuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "jdoe", "address": "10.1.1.1"})

    async with _client(handler) as c:
        r = await c.security.networkuser.create({"name": "jdoe", "address": "10.1.1.1"})
        assert r.name == "jdoe"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"jdoe"' in body


async def test_networkuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "jdoe", "address": "10.1.1.1"})

    async with _client(handler) as c:
        obj = Networkuser(
            **{
                "_ref": REF,
                "name": "jdoe",
                "address": "10.1.1.1",
                "user_status": "ACTIVE",
                "network": "10.1.1.0/24",
                "uuid": "ro-uuid",
                "data_source": "AD",
            }
        )
        await c.security.networkuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"user_status"' not in body, "user_status is readonly - must be stripped"
        assert '"network"' not in body, "network is readonly - must be stripped"
        assert '"data_source"' not in body, "data_source is readonly - must be stripped"
        assert '"jdoe"' in body
        assert '"10.1.1.1"' in body


async def test_networkuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.networkuser.delete(REF)
        assert result == REF
