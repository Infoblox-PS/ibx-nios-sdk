# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevicecomponentResource - list, get, find_one, type_ alias, readonly, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_devicecomponent import DiscoveryDevicecomponent
from tests.conftest import json_response

WAPI_TYPE = "discovery:devicecomponent"
REF = f"{WAPI_TYPE}/ZG5z:dc1"


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


async def test_discovery_devicecomponent_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "component_name": "FAN1", "type": "FAN"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.devicecomponent.list().all()
        assert len(records) == 1
        assert records[0].component_name == "FAN1"
        assert records[0].type_ == "FAN"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_devicecomponent_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "component_name": "FAN1", "device": "dev/ZG5z:d1"})
    ) as c:
        r = await c.discovery.devicecomponent.get(REF)
        assert r.component_name == "FAN1"
        assert r.device == "dev/ZG5z:d1"


async def test_discovery_devicecomponent_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "component_name": "FAN1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.devicecomponent.find_one()
        assert r is not None
        assert r.component_name == "FAN1"


async def test_discovery_devicecomponent_type_alias() -> None:
    obj = DiscoveryDevicecomponent(**{"_ref": REF, "type": "MODULE", "component_name": "MOD1"})
    assert obj.type_ == "MODULE"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "type" in dumped
    assert dumped["type"] == "MODULE"


async def test_discovery_devicecomponent_readonly_check() -> None:
    from ibx_nios_sdk.discovery._discovery_devicecomponent import DiscoveryDevicecomponentResource

    assert "component_name" in DiscoveryDevicecomponentResource._readonly_fields
    assert "device" in DiscoveryDevicecomponentResource._readonly_fields


async def test_discovery_devicecomponent_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_devicecomponent import DiscoveryDevicecomponentResource

    assert DiscoveryDevicecomponentResource._wapi_type == "discovery:devicecomponent"
