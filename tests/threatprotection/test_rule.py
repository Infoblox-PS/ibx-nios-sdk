# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRuleResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_rule import ThreatprotectionRule
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:rule"
REF = f"{WAPI_TYPE}/ZG5z:rule1"
MEMBER_REF = "member:grid/ZG5z:gm.example.com"
RULE_REF = "threatprotection:ruletemplate/ZG5z:tmpl1"


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


# 1. list with member filter
async def test_rule_list() -> None:
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
                        "member": MEMBER_REF,
                        "rule": RULE_REF,
                        "disable": False,
                        "sid": 9000001,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.rule.list(member=MEMBER_REF).all()
        assert len(records) == 1
        r = records[0]
        assert r.member == MEMBER_REF
        assert r.rule == RULE_REF
        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["member"] == MEMBER_REF


# 2. get by ref
async def test_rule_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "member": MEMBER_REF,
                "rule": RULE_REF,
                "disable": False,
                "sid": 9000001,
                "uuid": "some-uuid",
            }
        )
    ) as c:
        r = await c.threatprotection.rule.get(REF)
        assert r.member == MEMBER_REF
        assert r.sid == 9000001
        assert r.uuid == "some-uuid"


# 3. find_one
async def test_rule_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "member": MEMBER_REF,
                        "rule": RULE_REF,
                        "disable": False,
                        "sid": 9000001,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.rule.find_one(member=MEMBER_REF)
        assert r is not None
        assert r.rule == RULE_REF


# 4. create (WapiResource base supports it; WAPI may reject but SDK allows)
async def test_rule_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "member": MEMBER_REF,
                "rule": RULE_REF,
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.threatprotection.rule.create({"member": MEMBER_REF, "rule": RULE_REF})
        assert r.member == MEMBER_REF
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"member"' in body


# 5. update strips readonly
async def test_rule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "member": MEMBER_REF,
                "rule": RULE_REF,
                "disable": True,
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionRule(
            member=MEMBER_REF,
            rule=RULE_REF,
            sid=9000001,
            uuid="ro-uuid",
            disable=True,
        )
        await c.threatprotection.rule.update(REF, obj)
        body = captured[0].content.decode()
        assert '"member"' not in body, "member is readonly - must be stripped"
        assert '"rule"' not in body, "rule is readonly - must be stripped"
        assert '"sid"' not in body, "sid is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"disable":true' in body


# 6. delete
async def test_rule_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatprotection.rule.delete(REF)
        assert result == REF
