# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzPtrResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.rpz.models.record_rpz_ptr import RecordRpzPtr
from tests.conftest import json_response

WAPI_TYPE = "record:rpz:ptr"
REF = f"{WAPI_TYPE}/ZG5z:1.0.0.127.in-addr.arpa/default"


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


async def test_record_rpz_ptr_list() -> None:
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
                        "name": "1.0.0.127.in-addr.arpa",
                        "ptrdname": "blocked.example.com",
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
        records = await c.rpz.record_rpz_ptr.list(zone="rpz.example.com").all()
        assert len(records) == 1
        assert records[0].ptrdname == "blocked.example.com"
        assert captured[0].url.params["zone"] == "rpz.example.com"


async def test_record_rpz_ptr_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "1.0.0.127.in-addr.arpa",
                "ptrdname": "blocked.example.com",
                "ipv4addr": "127.0.0.1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "loopback blocked",
                "disable": False,
            }
        )
    ) as c:
        r = await c.rpz.record_rpz_ptr.get(REF)
        assert r.ptrdname == "blocked.example.com"
        assert r.ipv4addr == "127.0.0.1"


async def test_record_rpz_ptr_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "1.0.0.127.in-addr.arpa",
                        "ptrdname": "blocked.example.com",
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
        r = await c.rpz.record_rpz_ptr.find_one(ptrdname="blocked.example.com")
        assert r is not None
        assert r.ptrdname == "blocked.example.com"


async def test_record_rpz_ptr_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "1.0.0.127.in-addr.arpa",
                "ptrdname": "blocked.example.com",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.rpz.record_rpz_ptr.create(
            {"name": "1.0.0.127.in-addr.arpa", "ptrdname": "blocked.example.com"}
        )
        assert r.ptrdname == "blocked.example.com"
        assert captured[0].method == "POST"
        assert captured[0].url.params.get("_return_as_object") == "1"


async def test_record_rpz_ptr_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "1.0.0.127.in-addr.arpa",
                "ptrdname": "blocked.example.com",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "new",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        obj = RecordRpzPtr(
            name="1.0.0.127.in-addr.arpa",
            ptrdname="blocked.example.com",
            comment="new",
            uuid="ro-uuid",
            zone="rpz.example.com",
        )
        await c.rpz.record_rpz_ptr.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"ptrdname":"blocked.example.com"' in body


async def test_record_rpz_ptr_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.rpz.record_rpz_ptr.delete(REF)
        assert result == REF
