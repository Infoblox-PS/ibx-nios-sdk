# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TftpfiledirResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.tftpfiledir import Tftpfiledir
from tests.conftest import json_response

WAPI_TYPE = "tftpfiledir"
REF = f"{WAPI_TYPE}/ZG5z:tftp1"


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


async def test_tftpfiledir_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "tftp1", "type": "DIR", "directory": "/tftp"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.tftpfiledir.list().all()
        assert len(records) == 1
        assert records[0].name == "tftp1"
        assert records[0].type == "DIR"
        assert captured[0].url.params["_paging"] == "1"


async def test_tftpfiledir_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "tftp1", "type": "DIR", "directory": "/tftp"})
    ) as c:
        r = await c.misc.tftpfiledir.get(REF)
        assert r.name == "tftp1"
        assert r.ref == REF


async def test_tftpfiledir_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "tftp1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.tftpfiledir.find_one(name="tftp1")
        assert r is not None
        assert r.name == "tftp1"


async def test_tftpfiledir_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "tftp1"})

    async with _client(handler) as c:
        r = await c.misc.tftpfiledir.create({"name": "tftp1", "type": "DIR", "directory": "/tftp"})
        assert r.name == "tftp1"
        req = captured[0]
        assert req.method == "POST"
        assert '"tftp1"' in req.content.decode()


async def test_tftpfiledir_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "tftp1"})

    async with _client(handler) as c:
        obj = Tftpfiledir(
            **{
                "_ref": REF,
                "name": "tftp1",
                "is_synced_to_gm": True,
                "last_modify": 1700000000,
            }
        )
        await c.misc.tftpfiledir.update(REF, obj)
        body = captured[0].content.decode()
        assert '"is_synced_to_gm"' not in body, "is_synced_to_gm is readonly - must be stripped"
        assert '"last_modify"' not in body, "last_modify is readonly - must be stripped"
        assert '"tftp1"' in body


async def test_tftpfiledir_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.tftpfiledir.delete(REF)
        assert result == REF
