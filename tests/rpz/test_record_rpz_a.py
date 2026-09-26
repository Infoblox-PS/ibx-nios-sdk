# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzAResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.rpz.models.record_rpz_a import RecordRpzA
from tests.conftest import json_response

WAPI_TYPE = "record:rpz:a"
REF = f"{WAPI_TYPE}/ZG5z:bad.rpz.example.com/default"


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


# 1. list with zone filter
async def test_record_rpz_a_list() -> None:
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
                        "name": "bad.rpz.example.com",
                        "ipv4addr": "127.0.0.1",
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
        records = await c.rpz.record_rpz_a.list(zone="rpz.example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "bad.rpz.example.com"
        assert r.ipv4addr == "127.0.0.1"
        assert r.zone == "rpz.example.com"
        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["zone"] == "rpz.example.com"


# 2. get by ref
async def test_record_rpz_a_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "ipv4addr": "127.0.0.1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "blocked",
                "disable": False,
            }
        )
    ) as c:
        r = await c.rpz.record_rpz_a.get(REF)
        assert r.name == "bad.rpz.example.com"
        assert r.ipv4addr == "127.0.0.1"
        assert r.comment == "blocked"


# 3. find_one
async def test_record_rpz_a_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "bad.rpz.example.com",
                        "ipv4addr": "127.0.0.1",
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
        r = await c.rpz.record_rpz_a.find_one(name="bad.rpz.example.com")
        assert r is not None
        assert r.name == "bad.rpz.example.com"


# 4. create
async def test_record_rpz_a_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "ipv4addr": "127.0.0.1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.rpz.record_rpz_a.create(
            {"name": "bad.rpz.example.com", "ipv4addr": "127.0.0.1"}
        )
        assert r.name == "bad.rpz.example.com"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"
        body = req.content.decode()
        assert '"name":"bad.rpz.example.com"' in body


# 5. update strips readonly
async def test_record_rpz_a_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "ipv4addr": "127.0.0.1",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "new",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        obj = RecordRpzA(
            name="bad.rpz.example.com",
            comment="new",
            ipv4addr="127.0.0.1",
            uuid="ro-uuid",
            zone="rpz.example.com",
        )
        await c.rpz.record_rpz_a.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"zone"' not in body, "zone is readonly - must be stripped"
        assert '"name":"bad.rpz.example.com"' in body
        assert '"comment":"new"' in body


# 6. delete
async def test_record_rpz_a_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.rpz.record_rpz_a.delete(REF)
        assert result == REF
