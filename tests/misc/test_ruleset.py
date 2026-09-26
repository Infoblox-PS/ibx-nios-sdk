# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RulesetResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.ruleset import Ruleset
from tests.conftest import json_response

WAPI_TYPE = "ruleset"
REF = f"{WAPI_TYPE}/ZG5z:rs1"


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


async def test_ruleset_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "name": "rs1", "comment": "ruleset1", "type": "NXDOMAIN"}
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.ruleset.list().all()
        assert len(records) == 1
        assert records[0].name == "rs1"
        assert records[0].type == "NXDOMAIN"
        assert captured[0].url.params["_paging"] == "1"


async def test_ruleset_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "rs1", "comment": "ruleset1", "type": "NXDOMAIN"})
    ) as c:
        r = await c.misc.ruleset.get(REF)
        assert r.name == "rs1"
        assert r.ref == REF


async def test_ruleset_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "rs1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.ruleset.find_one(name="rs1")
        assert r is not None
        assert r.name == "rs1"


async def test_ruleset_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "rs1"})

    async with _client(handler) as c:
        r = await c.misc.ruleset.create({"name": "rs1", "type": "NXDOMAIN"})
        assert r.name == "rs1"
        req = captured[0]
        assert req.method == "POST"
        assert '"rs1"' in req.content.decode()


async def test_ruleset_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "rs1"})

    async with _client(handler) as c:
        obj = Ruleset(**{"_ref": REF, "name": "rs1", "uuid": "ro-uuid"})
        await c.misc.ruleset.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"rs1"' in body


async def test_ruleset_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.ruleset.delete(REF)
        assert result == REF
