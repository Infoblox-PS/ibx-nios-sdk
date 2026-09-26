# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverDnsResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.microsoftserver.models.msserver_dns import MsserverDns
from tests.conftest import json_response

WAPI_TYPE = "msserver:dns"
REF = f"{WAPI_TYPE}/ZG5z:dns1"


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


async def test_msserver_dns_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "address": "10.0.0.10"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.microsoftserver.dns.list().all()
        assert len(records) == 1
        assert records[0].address == "10.0.0.10"
        assert captured[0].url.params["_paging"] == "1"


async def test_msserver_dns_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "address": "10.0.0.10", "synchronization_interval": 7200})
    ) as c:
        r = await c.microsoftserver.dns.get(REF)
        assert r.synchronization_interval == 7200


async def test_msserver_dns_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "address": "10.0.0.10"}], "next_page_id": ""})
    ) as c:
        r = await c.microsoftserver.dns.find_one()
        assert r is not None


async def test_msserver_dns_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "address": "10.0.0.10"})

    async with _client(handler) as c:
        r = await c.microsoftserver.dns.create({"synchronization_interval": 7200})
        assert r.ref == REF
        assert captured[0].method == "POST"


async def test_msserver_dns_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = MsserverDns(
            **{
                "_ref": REF,
                "address": "10.0.0.10",
                "uuid": "ro-uuid",
                "synchronization_interval": 7200,
                "enable_dns_reports_sync": True,
            }
        )
        await c.microsoftserver.dns.update(REF, obj)
        body = captured[0].content.decode()
        assert '"address"' not in body, "address is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert "7200" in body


async def test_msserver_dns_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.microsoftserver.dns.delete(REF)
        assert result == REF
