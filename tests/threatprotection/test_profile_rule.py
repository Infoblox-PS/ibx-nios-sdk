# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionProfileRuleResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_profile_rule import (
    ThreatprotectionProfileRule,
)
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:profile:rule"
REF = f"{WAPI_TYPE}/ZG5z:rule1"
PROFILE_REF = "threatprotection:profile/ZG5z:myprofile"
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


# 1. list with profile filter
async def test_profile_rule_list() -> None:
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
                        "profile": PROFILE_REF,
                        "rule": RULE_REF,
                        "disable": False,
                        "sid": 9000001,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.profile_rule.list(profile=PROFILE_REF).all()
        assert len(records) == 1
        r = records[0]
        assert r.profile == PROFILE_REF
        assert r.rule == RULE_REF
        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["profile"] == PROFILE_REF


# 2. get by ref
async def test_profile_rule_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "profile": PROFILE_REF,
                "rule": RULE_REF,
                "disable": True,
                "sid": 9000001,
            }
        )
    ) as c:
        r = await c.threatprotection.profile_rule.get(REF)
        assert r.profile == PROFILE_REF
        assert r.disable is True


# 3. find_one
async def test_profile_rule_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "profile": PROFILE_REF,
                        "rule": RULE_REF,
                        "disable": False,
                        "sid": 9000001,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.profile_rule.find_one(profile=PROFILE_REF)
        assert r is not None
        assert r.rule == RULE_REF


# 4. create (WapiResource base supports it; WAPI may reject but SDK allows)
async def test_profile_rule_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "profile": PROFILE_REF,
                "rule": RULE_REF,
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.threatprotection.profile_rule.create(
            {"profile": PROFILE_REF, "rule": RULE_REF}
        )
        assert r.profile == PROFILE_REF
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"profile"' in body


# 5. update strips readonly
async def test_profile_rule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "profile": PROFILE_REF,
                "rule": RULE_REF,
                "disable": True,
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionProfileRule(
            profile=PROFILE_REF,
            rule=RULE_REF,
            sid=9000001,
            disable=True,
        )
        await c.threatprotection.profile_rule.update(REF, obj)
        body = captured[0].content.decode()
        assert '"profile"' not in body, "profile is readonly - must be stripped"
        assert '"rule"' not in body, "rule is readonly - must be stripped"
        assert '"sid"' not in body, "sid is readonly - must be stripped"
        assert '"disable":true' in body


# 6. delete
async def test_profile_rule_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatprotection.profile_rule.delete(REF)
        assert result == REF
