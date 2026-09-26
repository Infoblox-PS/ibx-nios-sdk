# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightCloudclientResource - list, get, find_one, create, update_strips_readonly, delete.

Note: The WAPI only supports GET (list/get) and PUT for this resource. create() and
delete() will make POST/DELETE requests - the mock transport accepts them at the SDK
level (WapiResource does not restrict methods). These tests verify the SDK layer only.
"""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatinsight.models.threatinsight_cloudclient import ThreatinsightCloudclient
from tests.conftest import json_response

WAPI_TYPE = "threatinsight:cloudclient"
REF = f"{WAPI_TYPE}/ZG5z:cloudclient"


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
async def test_cloudclient_list() -> None:
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
                        "enable": True,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatinsight.cloudclient.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.enable is True
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_cloudclient_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "enable": False,
                "interval": 300,
                "blacklist_rpz_list": [],
            }
        )
    ) as c:
        r = await c.threatinsight.cloudclient.get(REF)
        assert r.enable is False
        assert r.interval == 300


# 3. find_one
async def test_cloudclient_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "enable": True,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatinsight.cloudclient.find_one(enable=True)
        assert r is not None
        assert r.enable is True


# 4. create (POST at SDK level - WAPI may not support it, but SDK layer must work)
async def test_cloudclient_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "enable": True,
            }
        )

    async with _client(handler) as c:
        r = await c.threatinsight.cloudclient.create({"enable": True})
        assert r.enable is True
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"enable":true' in body


# 5. update strips readonly
async def test_cloudclient_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "enable": True,
            }
        )

    async with _client(handler) as c:
        obj = ThreatinsightCloudclient(
            enable=True,
            uuid="ro-uuid",
            interval=600,
        )
        await c.threatinsight.cloudclient.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"enable":true' in body
        assert '"interval":600' in body


# 6. delete (DELETE at SDK level)
async def test_cloudclient_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.threatinsight.cloudclient.delete(REF)
        assert result == REF
