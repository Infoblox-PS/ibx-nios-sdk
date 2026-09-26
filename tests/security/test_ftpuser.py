# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FtpuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.ftpuser import Ftpuser
from tests.conftest import json_response

WAPI_TYPE = "ftpuser"
REF = f"{WAPI_TYPE}/ZG5z:ftpuser1"


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


async def test_ftpuser_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "username": "ftpuser1", "home_dir": "/home/ftpuser1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.ftpuser.list().all()
        assert len(records) == 1
        assert records[0].username == "ftpuser1"
        assert captured[0].url.params["_paging"] == "1"


async def test_ftpuser_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "username": "ftpuser1",
                "home_dir": "/home/ftpuser1",
                "permission": "RW",
            }
        )
    ) as c:
        r = await c.security.ftpuser.get(REF)
        assert r.username == "ftpuser1"
        assert r.permission == "RW"


async def test_ftpuser_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "username": "ftpuser1", "home_dir": "/home/ftpuser1"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.ftpuser.find_one(username="ftpuser1")
        assert r is not None
        assert r.username == "ftpuser1"


async def test_ftpuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "username": "ftpuser1", "home_dir": "/home/ftpuser1"})

    async with _client(handler) as c:
        r = await c.security.ftpuser.create({"username": "ftpuser1", "home_dir": "/home/ftpuser1"})
        assert r.username == "ftpuser1"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"ftpuser1"' in body


async def test_ftpuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "username": "ftpuser1"})

    async with _client(handler) as c:
        obj = Ftpuser(
            **{
                "_ref": REF,
                "username": "ftpuser1",
                "home_dir": "/home/ftpuser1",
                "uuid": "ro-uuid",
                "permission": "RW",
            }
        )
        await c.security.ftpuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"username"' not in body, "username is create-only on ftpuser - stripped on update"
        assert '"home_dir"' not in body, "home_dir is create-only on ftpuser - stripped on update"
        assert '"permission"' in body


async def test_ftpuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.ftpuser.delete(REF)
        assert result == REF
