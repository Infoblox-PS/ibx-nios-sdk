# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzAaaaIpaddressResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.rpz.models.record_rpz_aaaa_ipaddress import RecordRpzAaaaIpaddress
from tests.conftest import json_response

WAPI_TYPE = "record:rpz:aaaa:ipaddress"
REF = f"{WAPI_TYPE}/ZG5z:1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.rpz-ip.rpz.example.com/default"


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


async def test_record_rpz_aaaa_ipaddress_list() -> None:
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
                        "name": "::1.rpz-ip.rpz.example.com",
                        "ipv6addr": "::1",
                        "view": "default",
                        "zone": "rpz.example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.rpz.record_rpz_aaaa_ipaddress.list(zone="rpz.example.com").all()
        assert len(records) == 1
        assert records[0].ipv6addr == "::1"
        assert captured[0].url.params["zone"] == "rpz.example.com"


async def test_record_rpz_aaaa_ipaddress_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "::1.rpz-ip.rpz.example.com",
                "ipv6addr": "::1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "ipv6 blocked",
                "disable": False,
            }
        )
    ) as c:
        r = await c.rpz.record_rpz_aaaa_ipaddress.get(REF)
        assert r.ipv6addr == "::1"
        assert r.comment == "ipv6 blocked"


async def test_record_rpz_aaaa_ipaddress_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "::1.rpz-ip.rpz.example.com",
                        "ipv6addr": "::1",
                        "view": "default",
                        "zone": "rpz.example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.rpz.record_rpz_aaaa_ipaddress.find_one(ipv6addr="::1")
        assert r is not None
        assert r.ipv6addr == "::1"


async def test_record_rpz_aaaa_ipaddress_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "::1.rpz-ip.rpz.example.com",
                "ipv6addr": "::1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.rpz.record_rpz_aaaa_ipaddress.create(
            {"name": "::1.rpz-ip.rpz.example.com", "ipv6addr": "::1"}
        )
        assert r.ipv6addr == "::1"
        assert captured[0].method == "POST"
        assert captured[0].url.params.get("_return_as_object") == "1"


async def test_record_rpz_aaaa_ipaddress_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "::1.rpz-ip.rpz.example.com",
                "ipv6addr": "::1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "new",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        obj = RecordRpzAaaaIpaddress(
            name="::1.rpz-ip.rpz.example.com",
            comment="new",
            ipv6addr="::1",
            uuid="ro-uuid",
            zone="rpz.example.com",
        )
        await c.rpz.record_rpz_aaaa_ipaddress.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"ipv6addr":"::1"' in body


async def test_record_rpz_aaaa_ipaddress_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.rpz.record_rpz_aaaa_ipaddress.delete(REF)
        assert result == REF
