# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryGridpropertiesResource - list, get, find_one, update, readonly, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_gridproperties import DiscoveryGridproperties
from tests.conftest import json_response

WAPI_TYPE = "discovery:gridproperties"
REF = f"{WAPI_TYPE}/ZG5z:gp1"


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


async def test_discovery_gridproperties_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "grid_name": "Infoblox"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.discovery.gridproperties.list().all()
        assert len(records) == 1
        assert records[0].grid_name == "Infoblox"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_gridproperties_get() -> None:
    async with _client(_session_handler({"_ref": REF, "grid_name": "Infoblox"})) as c:
        r = await c.discovery.gridproperties.get(REF)
        assert r.grid_name == "Infoblox"


async def test_discovery_gridproperties_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "grid_name": "Infoblox"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.gridproperties.find_one()
        assert r is not None


async def test_discovery_gridproperties_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DiscoveryGridproperties(
            **{
                "_ref": REF,
                "grid_name": "Infoblox",
                "uuid": "ro-uuid",
                "enable_auto_updates": True,
            }
        )
        await c.discovery.gridproperties.update(REF, obj)
        body = captured[0].content.decode()
        assert '"grid_name"' not in body, "grid_name is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert "true" in body.lower()  # enable_auto_updates


async def test_discovery_gridproperties_model_nested() -> None:
    """Nested settings stored as dict[str, Any]."""
    obj = DiscoveryGridproperties(
        **{
            "_ref": REF,
            "basic_polling_settings": {"polling_interval": 60},
            "dns_lookup_option": "DISABLED",
        }
    )
    assert obj.basic_polling_settings == {"polling_interval": 60}
    assert obj.dns_lookup_option == "DISABLED"


async def test_discovery_gridproperties_wapi_type() -> None:
    from ibx_nios_sdk.discovery._discovery_gridproperties import DiscoveryGridpropertiesResource

    assert DiscoveryGridpropertiesResource._wapi_type == "discovery:gridproperties"
