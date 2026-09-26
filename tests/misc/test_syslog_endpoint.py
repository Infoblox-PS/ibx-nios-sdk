# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SyslogEndpointResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.syslog_endpoint import SyslogEndpoint
from tests.conftest import json_response

WAPI_TYPE = "syslog:endpoint"
REF = f"{WAPI_TYPE}/ZG5z:syslog1"


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


async def test_syslog_endpoint_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "syslog1", "log_level": "INFO", "timeout": 30}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.syslog_endpoint.list().all()
        assert len(records) == 1
        assert records[0].name == "syslog1"
        assert captured[0].url.params["_paging"] == "1"


async def test_syslog_endpoint_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "syslog1", "log_level": "INFO"})
    ) as c:
        r = await c.misc.syslog_endpoint.get(REF)
        assert r.name == "syslog1"
        assert r.ref == REF


async def test_syslog_endpoint_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "syslog1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.syslog_endpoint.find_one(name="syslog1")
        assert r is not None
        assert r.name == "syslog1"


async def test_syslog_endpoint_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "syslog1"})

    async with _client(handler) as c:
        r = await c.misc.syslog_endpoint.create({"name": "syslog1", "log_level": "INFO"})
        assert r.name == "syslog1"
        req = captured[0]
        assert req.method == "POST"
        assert '"syslog1"' in req.content.decode()


async def test_syslog_endpoint_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "syslog1"})

    async with _client(handler) as c:
        obj = SyslogEndpoint(**{"_ref": REF, "name": "syslog1", "uuid": "ro-uuid"})
        await c.misc.syslog_endpoint.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"syslog1"' in body


async def test_syslog_endpoint_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.syslog_endpoint.delete(REF)
        assert result == REF
