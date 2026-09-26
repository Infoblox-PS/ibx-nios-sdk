# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionProfileResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_profile import ThreatprotectionProfile
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:profile"
REF = f"{WAPI_TYPE}/ZG5z:myprofile"


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
async def test_profile_list() -> None:
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
                        "name": "myprofile",
                        "comment": "test profile",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.profile.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "myprofile"
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_profile_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "myprofile",
                "comment": "test profile",
                "current_ruleset": "v1.0",
            }
        )
    ) as c:
        r = await c.threatprotection.profile.get(REF)
        assert r.name == "myprofile"
        assert r.current_ruleset == "v1.0"


# 3. find_one
async def test_profile_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "myprofile",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.profile.find_one(name="myprofile")
        assert r is not None
        assert r.name == "myprofile"


# 4. create
async def test_profile_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "myprofile",
                "comment": "created",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.threatprotection.profile.create({"name": "myprofile", "comment": "created"})
        assert r.name == "myprofile"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"
        body = req.content.decode()
        assert '"name":"myprofile"' in body


# 5. update strips readonly
async def test_profile_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "myprofile",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionProfile(
            name="myprofile",
            uuid="ro-uuid",
            comment="updated",
        )
        await c.threatprotection.profile.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"name":"myprofile"' in body
        assert '"comment":"updated"' in body


# 6. delete
async def test_profile_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatprotection.profile.delete(REF)
        assert result == REF
