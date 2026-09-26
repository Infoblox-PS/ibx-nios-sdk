# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzTxtResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.rpz.models.record_rpz_txt import RecordRpzTxt
from tests.conftest import json_response

WAPI_TYPE = "record:rpz:txt"
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


async def test_record_rpz_txt_list() -> None:
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
                        "text": "blocked by rpz",
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
        records = await c.rpz.record_rpz_txt.list(zone="rpz.example.com").all()
        assert len(records) == 1
        assert records[0].text == "blocked by rpz"
        assert captured[0].url.params["zone"] == "rpz.example.com"


async def test_record_rpz_txt_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "text": "blocked by rpz",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "rpz txt",
                "disable": False,
            }
        )
    ) as c:
        r = await c.rpz.record_rpz_txt.get(REF)
        assert r.text == "blocked by rpz"
        assert r.comment == "rpz txt"


async def test_record_rpz_txt_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "bad.rpz.example.com",
                        "text": "blocked by rpz",
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
        r = await c.rpz.record_rpz_txt.find_one(name="bad.rpz.example.com")
        assert r is not None
        assert r.text == "blocked by rpz"


async def test_record_rpz_txt_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "text": "blocked by rpz",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.rpz.record_rpz_txt.create(
            {"name": "bad.rpz.example.com", "text": "blocked by rpz"}
        )
        assert r.text == "blocked by rpz"
        assert captured[0].method == "POST"
        assert captured[0].url.params.get("_return_as_object") == "1"


async def test_record_rpz_txt_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "text": "blocked by rpz",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "new",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        obj = RecordRpzTxt(
            name="bad.rpz.example.com",
            text="blocked by rpz",
            comment="new",
            uuid="ro-uuid",
            zone="rpz.example.com",
        )
        await c.rpz.record_rpz_txt.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"text":"blocked by rpz"' in body


async def test_record_rpz_txt_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.rpz.record_rpz_txt.delete(REF)
        assert result == REF
