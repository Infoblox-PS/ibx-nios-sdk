# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.microsoftserver.models.msserver import Msserver
from tests.conftest import json_response

WAPI_TYPE = "msserver"
REF = f"{WAPI_TYPE}/ZG5z:ms1"


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


async def test_msserver_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "address": "10.0.0.10", "server_name": "dc1.corp.com"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.microsoftserver.msserver.list().all()
        assert len(records) == 1
        assert records[0].address == "10.0.0.10"
        assert records[0].server_name == "dc1.corp.com"
        assert captured[0].url.params["_paging"] == "1"


async def test_msserver_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "address": "10.0.0.10", "comment": "corp DC"})
    ) as c:
        r = await c.microsoftserver.msserver.get(REF)
        assert r.address == "10.0.0.10"
        assert r.comment == "corp DC"


async def test_msserver_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "address": "10.0.0.10"}], "next_page_id": ""})
    ) as c:
        r = await c.microsoftserver.msserver.find_one(address="10.0.0.10")
        assert r is not None
        assert r.address == "10.0.0.10"


async def test_msserver_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "address": "10.0.0.10"})

    async with _client(handler) as c:
        r = await c.microsoftserver.msserver.create({"address": "10.0.0.10"})
        assert r.address == "10.0.0.10"
        assert captured[0].method == "POST"
        assert '"10.0.0.10"' in captured[0].content.decode()


async def test_msserver_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = Msserver(
            **{
                "_ref": REF,
                "address": "10.0.0.10",
                "comment": "corp DC",
                "connection_status": "CONNECTED",
                "uuid": "ro-uuid",
                "version": "2019",
                "last_seen": 1700000000,
                "synchronization_status": "OK",
            }
        )
        await c.microsoftserver.msserver.update(REF, obj)
        body = captured[0].content.decode()
        assert '"connection_status"' not in body, (
            "connection_status is readonly - must be stripped"
        )
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"version"' not in body, "version is readonly - must be stripped"
        assert '"corp DC"' in body


async def test_msserver_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.microsoftserver.msserver.delete(REF)
        assert result == REF
