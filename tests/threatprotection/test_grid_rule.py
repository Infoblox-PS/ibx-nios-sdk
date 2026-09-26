# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionGridRuleResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.grid_threatprotection_rule import (
    ThreatprotectionGridRule,
)
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:grid:rule"
REF = f"{WAPI_TYPE}/ZG5z:rule1"


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


# 1. list
async def test_grid_rule_list() -> None:
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
                        "name": "rule-1",
                        "template": "tmpl1",
                        "comment": "test rule",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.grid_rule.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "rule-1"
        assert r.template == "tmpl1"
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_grid_rule_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "rule-1",
                "template": "tmpl1",
                "comment": "test rule",
                "disable": False,
                "sid": 9000001,
            }
        )
    ) as c:
        r = await c.threatprotection.grid_rule.get(REF)
        assert r.name == "rule-1"
        assert r.sid == 9000001


# 3. find_one
async def test_grid_rule_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "rule-1",
                        "template": "tmpl1",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.grid_rule.find_one(name="rule-1")
        assert r is not None
        assert r.name == "rule-1"


# 4. create
async def test_grid_rule_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "rule-1",
                "template": "tmpl1",
                "comment": "created",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.threatprotection.grid_rule.create({"template": "tmpl1", "comment": "created"})
        assert r.template == "tmpl1"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"
        body = req.content.decode()
        assert '"comment":"created"' in body


# 5. update strips readonly
async def test_grid_rule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "rule-1",
                "template": "tmpl1",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionGridRule(
            name="rule-1",
            sid=9000001,
            category="CUSTOM",
            uuid="ro-uuid",
            description="some desc",
            comment="updated",
            template="tmpl1",
        )
        await c.threatprotection.grid_rule.update(REF, obj)
        body = captured[0].content.decode()
        assert '"sid"' not in body, "sid is readonly - must be stripped"
        assert '"category"' not in body, "category is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"description"' not in body, "description is readonly - must be stripped"
        assert '"comment":"updated"' in body
        assert '"template":"tmpl1"' in body


# 6. delete
async def test_grid_rule_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatprotection.grid_rule.delete(REF)
        assert result == REF
