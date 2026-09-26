# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolBlockingpolicyResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.parentalcontrol_blockingpolicy import (
    ParentalcontrolBlockingpolicy,
)
from tests.conftest import json_response

WAPI_TYPE = "parentalcontrol:blockingpolicy"
REF = f"{WAPI_TYPE}/ZG5z:policy1"


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


async def test_parentalcontrol_blockingpolicy_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.security.parentalcontrol_blockingpolicy._wapi_type == WAPI_TYPE


async def test_parentalcontrol_blockingpolicy_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "policy1", "value": "block-val"}],
                "next_page_id": "",
            }
        )
    ) as c:
        items = await c.security.parentalcontrol_blockingpolicy.list().all()
        assert len(items) == 1
        assert items[0].name == "policy1"
        assert items[0].value == "block-val"


async def test_parentalcontrol_blockingpolicy_get_by_ref() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "policy1", "value": "v"})) as c:
        r = await c.security.parentalcontrol_blockingpolicy.get(REF)
        assert r.ref == REF
        assert r.name == "policy1"


async def test_parentalcontrol_blockingpolicy_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "policy1"}], "next_page_id": ""})
    ) as c:
        r = await c.security.parentalcontrol_blockingpolicy.find_one(name="policy1")
        assert r is not None
        assert r.name == "policy1"


async def test_parentalcontrol_blockingpolicy_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "policy1"})

    async with _client(handler) as c:
        r = await c.security.parentalcontrol_blockingpolicy.create(
            {"name": "policy1", "value": "block-val"}
        )
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"policy1"' in body


async def test_parentalcontrol_blockingpolicy_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "policy1"})

    async with _client(handler) as c:
        obj = ParentalcontrolBlockingpolicy(name="policy1", value="new-val", uuid="ro-uuid")
        await c.security.parentalcontrol_blockingpolicy.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"value":"new-val"' in body


async def test_parentalcontrol_blockingpolicy_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.security.parentalcontrol_blockingpolicy.delete(REF) == REF
