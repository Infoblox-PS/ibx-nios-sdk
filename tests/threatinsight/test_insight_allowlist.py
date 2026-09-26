# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightInsightAllowlistResource - list, get, find_one, create, update_strips_readonly, delete.

Note: The WAPI only supports GET (list/get) for this resource - it is fully read-only.
create(), update(), and delete() tests verify the SDK layer (WapiResource generic behaviour).
"""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatinsight.models.threatinsight_insight_allowlist import (
    ThreatinsightInsightAllowlist,
)
from tests.conftest import json_response

WAPI_TYPE = "threatinsight:insight_allowlist"
REF = f"{WAPI_TYPE}/ZG5z:insightallowlist"


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
async def test_insight_allowlist_list() -> None:
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
                        "version": "1.2.3",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatinsight.insight_allowlist.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.version == "1.2.3"
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_insight_allowlist_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "version": "2.0.0",
                "uuid": "some-uuid",
            }
        )
    ) as c:
        r = await c.threatinsight.insight_allowlist.get(REF)
        assert r.version == "2.0.0"
        assert r.uuid == "some-uuid"


# 3. find_one
async def test_insight_allowlist_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "version": "1.2.3",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatinsight.insight_allowlist.find_one(version="1.2.3")
        assert r is not None
        assert r.version == "1.2.3"


# 4. create (POST at SDK level - WAPI does not support this; SDK layer verified)
async def test_insight_allowlist_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "version": "1.0.0"})

    async with _client(handler) as c:
        r = await c.threatinsight.insight_allowlist.create({"version": "1.0.0"})
        assert r.version == "1.0.0"
        req = captured[0]
        assert req.method == "POST"


# 5. update strips readonly
async def test_insight_allowlist_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "version": "1.0.0"})

    async with _client(handler) as c:
        obj = ThreatinsightInsightAllowlist(uuid="ro-uuid", version="1.0.0")
        await c.threatinsight.insight_allowlist.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"version"' not in body, "version is readonly - must be stripped"


# 6. delete (DELETE at SDK level)
async def test_insight_allowlist_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatinsight.insight_allowlist.delete(REF)
        assert result == REF
