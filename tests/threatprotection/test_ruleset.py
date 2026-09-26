# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRulesetResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_ruleset import ThreatprotectionRuleset
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:ruleset"
REF = f"{WAPI_TYPE}/ZG5z:v1.0"


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


# 1. list
async def test_ruleset_list() -> None:
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
                        "version": "v1.0",
                        "comment": "initial ruleset",
                        "used_by": ["profile1"],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.ruleset.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.version == "v1.0"
        assert r.comment == "initial ruleset"
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_ruleset_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "version": "v1.0",
                "comment": "initial ruleset",
                "used_by": ["profile1", "profile2"],
                "add_type": "MANUAL",
                "added_time": 1700000000,
            }
        )
    ) as c:
        r = await c.threatprotection.ruleset.get(REF)
        assert r.version == "v1.0"
        assert r.add_type == "MANUAL"
        assert r.added_time == 1700000000


# 3. find_one
async def test_ruleset_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "version": "v1.0",
                        "comment": "",
                        "used_by": [],
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.ruleset.find_one(version="v1.0")
        assert r is not None
        assert r.version == "v1.0"


# 4. create (no POST in swagger but WapiResource supports it)
async def test_ruleset_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "version": "v1.0",
                "comment": "created",
            }
        )

    async with _client(handler) as c:
        r = await c.threatprotection.ruleset.create({"comment": "created"})
        assert r.comment == "created"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"comment":"created"' in body


# 5. update strips readonly
async def test_ruleset_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "version": "v1.0",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionRuleset(
            version="v1.0",
            add_type="MANUAL",
            added_time=1700000000,
            uuid="ro-uuid",
            used_by=["profile1"],
            comment="updated",
        )
        await c.threatprotection.ruleset.update(REF, obj)
        body = captured[0].content.decode()
        assert '"version"' not in body, "version is readonly - must be stripped"
        assert '"add_type"' not in body, "add_type is readonly - must be stripped"
        assert '"added_time"' not in body, "added_time is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"used_by"' not in body, "used_by is readonly - must be stripped"
        assert '"comment":"updated"' in body


# 6. delete
async def test_ruleset_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatprotection.ruleset.delete(REF)
        assert result == REF
