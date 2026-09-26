# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SnmpuserResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.snmpuser import Snmpuser
from tests.conftest import json_response

WAPI_TYPE = "snmpuser"
REF = f"{WAPI_TYPE}/ZG5z:snmp1"


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


async def test_snmpuser_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "snmpuser1", "comment": "snmp user"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.snmpuser.list().all()
        assert len(records) == 1
        assert records[0].name == "snmpuser1"
        assert captured[0].url.params["_paging"] == "1"


async def test_snmpuser_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "snmpuser1",
                "comment": "test",
                "authentication_protocol": "MD5",
            }
        )
    ) as c:
        r = await c.security.snmpuser.get(REF)
        assert r.name == "snmpuser1"
        assert r.authentication_protocol == "MD5"


async def test_snmpuser_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "snmpuser1", "comment": ""}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.snmpuser.find_one(name="snmpuser1")
        assert r is not None
        assert r.name == "snmpuser1"


async def test_snmpuser_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "snmpuser1", "comment": "created"})

    async with _client(handler) as c:
        r = await c.security.snmpuser.create({"name": "snmpuser1", "comment": "created"})
        assert r.name == "snmpuser1"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"snmpuser1"' in body


async def test_snmpuser_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "snmpuser1", "comment": "updated"})

    async with _client(handler) as c:
        obj = Snmpuser(
            **{"_ref": REF, "name": "snmpuser1", "comment": "updated", "uuid": "ro-uuid"}
        )
        await c.security.snmpuser.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"snmpuser1"' in body


async def test_snmpuser_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.snmpuser.delete(REF)
        assert result == REF
