# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevicesupportbundleResource - list, get, find_one, delete, readonly, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "discovery:devicesupportbundle"
REF = f"{WAPI_TYPE}/ZG5z:dsb1"


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


async def test_discovery_devicesupportbundle_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "bundle1", "version": "1.0.0"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.devicesupportbundle.list().all()
        assert len(records) == 1
        assert records[0].name == "bundle1"
        assert records[0].version == "1.0.0"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_devicesupportbundle_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "bundle1", "author": "Infoblox"})
    ) as c:
        r = await c.discovery.devicesupportbundle.get(REF)
        assert r.name == "bundle1"
        assert r.author == "Infoblox"


async def test_discovery_devicesupportbundle_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "bundle1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.devicesupportbundle.find_one(name="bundle1")
        assert r is not None
        assert r.name == "bundle1"


async def test_discovery_devicesupportbundle_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.discovery.devicesupportbundle.delete(REF)
        assert result == REF


async def test_discovery_devicesupportbundle_readonly_check() -> None:
    from ibx_nios_sdk.discovery._discovery_devicesupportbundle import (
        DiscoveryDevicesupportbundleResource,
    )

    assert "author" in DiscoveryDevicesupportbundleResource._readonly_fields
    assert "version" in DiscoveryDevicesupportbundleResource._readonly_fields


async def test_discovery_devicesupportbundle_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_devicesupportbundle import (
        DiscoveryDevicesupportbundleResource,
    )

    assert DiscoveryDevicesupportbundleResource._wapi_type == "discovery:devicesupportbundle"
