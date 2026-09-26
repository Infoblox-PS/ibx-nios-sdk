# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightAllowlistResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatinsight.models.threatinsight_allowlist import ThreatinsightAllowlist
from tests.conftest import json_response

WAPI_TYPE = "threatinsight:allowlist"
REF = f"{WAPI_TYPE}/ZG5z:myallowlist"


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
async def test_allowlist_list() -> None:
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
                        "fqdn": "bad.example.com",
                        "type": "CUSTOM",
                        "comment": "test entry",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatinsight.allowlist.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.fqdn == "bad.example.com"
        assert r.type_ == "CUSTOM"
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_allowlist_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "fqdn": "bad.example.com",
                "type": "SYSTEM",
                "comment": "system entry",
                "disable": False,
            }
        )
    ) as c:
        r = await c.threatinsight.allowlist.get(REF)
        assert r.fqdn == "bad.example.com"
        assert r.type_ == "SYSTEM"
        assert r.disable is False


# 3. find_one
async def test_allowlist_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "fqdn": "bad.example.com",
                        "type": "CUSTOM",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatinsight.allowlist.find_one(fqdn="bad.example.com")
        assert r is not None
        assert r.fqdn == "bad.example.com"


# 4. create
async def test_allowlist_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "fqdn": "bad.example.com",
                "type": "CUSTOM",
                "comment": "created",
            }
        )

    async with _client(handler) as c:
        r = await c.threatinsight.allowlist.create(
            {"fqdn": "bad.example.com", "comment": "created"}
        )
        assert r.fqdn == "bad.example.com"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"
        body = req.content.decode()
        assert '"fqdn":"bad.example.com"' in body


# 5. update strips readonly
async def test_allowlist_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "fqdn": "bad.example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        obj = ThreatinsightAllowlist(
            fqdn="bad.example.com",
            comment="updated",
            uuid="ro-uuid",
            **{"type": "CUSTOM"},
        )
        await c.threatinsight.allowlist.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"type"' not in body, "type is readonly - must be stripped"
        assert '"fqdn":"bad.example.com"' in body
        assert '"comment":"updated"' in body


# 6. delete
async def test_allowlist_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatinsight.allowlist.delete(REF)
        assert result == REF
