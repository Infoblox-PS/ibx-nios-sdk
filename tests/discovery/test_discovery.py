# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryResource - list, get, find_one, update, wapi_type check."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "discovery"
REF = f"{WAPI_TYPE}/ZG5z:disc1"


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


async def test_discovery_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.discovery.discovery.list().all()
        assert len(records) == 1
        assert records[0].ref == REF
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_get() -> None:
    async with _client(_session_handler({"_ref": REF})) as c:
        r = await c.discovery.discovery.get(REF)
        assert r.ref == REF


async def test_discovery_find_one() -> None:
    async with _client(_session_handler({"result": [{"_ref": REF}], "next_page_id": ""})) as c:
        r = await c.discovery.discovery.find_one()
        assert r is not None
        assert r.ref == REF


async def test_discovery_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        from ibx_nios_sdk.discovery.models.discovery import Discovery

        obj = Discovery(**{"_ref": REF})
        await c.discovery.discovery.update(REF, obj)
        assert captured[0].method == "PUT"


async def test_discovery_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery import DiscoveryResource

    assert DiscoveryResource._wapi_type == "discovery"


async def test_discovery_model_round_trip() -> None:
    from ibx_nios_sdk.discovery.models.discovery import Discovery

    obj = Discovery(**{"_ref": REF})
    assert obj.ref == REF
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "_ref" in dumped
