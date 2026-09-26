# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceResource - list, get, find_one, type_ alias, readonly check, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_device import DiscoveryDevice
from tests.conftest import json_response

WAPI_TYPE = "discovery:device"
REF = f"{WAPI_TYPE}/ZG5z:dev1"


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


async def test_discovery_device_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "dev1", "type": "SWITCH"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.discovery.device.list().all()
        assert len(records) == 1
        assert records[0].name == "dev1"
        assert records[0].type_ == "SWITCH"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_device_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "dev1", "address": "10.0.0.1"})
    ) as c:
        r = await c.discovery.device.get(REF)
        assert r.name == "dev1"
        assert r.address == "10.0.0.1"


async def test_discovery_device_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "dev1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.device.find_one(name="dev1")
        assert r is not None
        assert r.name == "dev1"


async def test_discovery_device_type_alias() -> None:
    """type_ must deserialise from the 'type' JSON key."""
    obj = DiscoveryDevice(**{"_ref": REF, "type": "ROUTER", "name": "dev1"})
    assert obj.type_ == "ROUTER"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "type" in dumped
    assert dumped["type"] == "ROUTER"


async def test_discovery_device_readonly_stripped_on_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DiscoveryDevice(
            **{
                "_ref": REF,
                "name": "dev1",
                "address": "10.0.0.1",
                "vendor": "Cisco",
                "privileged_polling": True,
            }
        )
        await c.discovery.device.update(REF, obj)
        body = captured[0].content.decode()
        assert '"address"' not in body, "address is readonly - must be stripped"
        assert '"vendor"' not in body, "vendor is readonly - must be stripped"
        assert '"name"' not in body, "name is readonly on discovery:device - must be stripped"
        assert '"privileged_polling"' in body


async def test_discovery_device_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_device import DiscoveryDeviceResource

    assert DiscoveryDeviceResource._wapi_type == "discovery:device"
