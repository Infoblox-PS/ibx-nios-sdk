# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""BfdtemplateResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.bfdtemplate import Bfdtemplate
from tests.conftest import json_response

WAPI_TYPE = "bfdtemplate"
REF = f"{WAPI_TYPE}/ZG5z:bfd1"


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


async def test_bfdtemplate_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "bfd1", "detection_multiplier": 3}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.bfdtemplate.list().all()
        assert len(records) == 1
        assert records[0].name == "bfd1"
        assert captured[0].url.params["_paging"] == "1"


async def test_bfdtemplate_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "bfd1", "detection_multiplier": 3})
    ) as c:
        r = await c.misc.bfdtemplate.get(REF)
        assert r.name == "bfd1"
        assert r.ref == REF


async def test_bfdtemplate_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "bfd1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.bfdtemplate.find_one(name="bfd1")
        assert r is not None
        assert r.name == "bfd1"


async def test_bfdtemplate_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "bfd1"})

    async with _client(handler) as c:
        r = await c.misc.bfdtemplate.create({"name": "bfd1", "detection_multiplier": 3})
        assert r.name == "bfd1"
        req = captured[0]
        assert req.method == "POST"
        assert '"bfd1"' in req.content.decode()


async def test_bfdtemplate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "bfd1"})

    async with _client(handler) as c:
        obj = Bfdtemplate(**{"_ref": REF, "name": "bfd1", "uuid": "ro-uuid"})
        await c.misc.bfdtemplate.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"bfd1"' in body


async def test_bfdtemplate_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.bfdtemplate.delete(REF)
        assert result == REF
