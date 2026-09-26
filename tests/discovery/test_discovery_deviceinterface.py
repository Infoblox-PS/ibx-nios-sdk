# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceinterfaceResource - list, get, find_one, type_ alias, update, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_deviceinterface import DiscoveryDeviceinterface
from tests.conftest import json_response

WAPI_TYPE = "discovery:deviceinterface"
REF = f"{WAPI_TYPE}/ZG5z:di1"


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


async def test_discovery_deviceinterface_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "eth0", "mac": "aa:bb:cc:dd:ee:ff"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.deviceinterface.list().all()
        assert len(records) == 1
        assert records[0].name == "eth0"
        assert records[0].mac == "aa:bb:cc:dd:ee:ff"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_deviceinterface_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "eth0", "oper_status": "UP"})) as c:
        r = await c.discovery.deviceinterface.get(REF)
        assert r.name == "eth0"
        assert r.oper_status == "UP"


async def test_discovery_deviceinterface_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "eth0"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.deviceinterface.find_one(name="eth0")
        assert r is not None
        assert r.name == "eth0"


async def test_discovery_deviceinterface_type_alias() -> None:
    obj = DiscoveryDeviceinterface(**{"_ref": REF, "type": "ETHERNET", "name": "eth0"})
    assert obj.type_ == "ETHERNET"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "type" in dumped


async def test_discovery_deviceinterface_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DiscoveryDeviceinterface(
            **{
                "_ref": REF,
                "mac": "aa:bb:cc:dd:ee:ff",
                "oper_status": "UP",
                "description": "my desc",
                "admin_status": "ENABLED",
                "extattrs": {"Site": {"value": "NYC"}},
            }
        )
        await c.discovery.deviceinterface.update(REF, obj)
        body = captured[0].content.decode()
        assert '"mac"' not in body, "mac is readonly - must be stripped"
        assert '"oper_status"' not in body, "oper_status is readonly - must be stripped"
        assert '"description"' not in body, "description is readonly on live schema"
        assert '"extattrs"' in body, "extattrs is the only writable field on deviceinterface"


async def test_discovery_deviceinterface_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_deviceinterface import DiscoveryDeviceinterfaceResource

    assert DiscoveryDeviceinterfaceResource._wapi_type == "discovery:deviceinterface"
