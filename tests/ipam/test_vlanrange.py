# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VlanrangeResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.vlanrange import Vlanrange
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns vlanrange objects
# ---------------------------------------------------------------------------


async def test_vlanrange_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlanrange/ZG5z:prod-range",
                        "name": "prod-range",
                        "vlan_view": "vlanview/ZG5z:default",
                        "start_vlan_id": 100,
                        "end_vlan_id": 200,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        ranges = await c.ipam.vlanrange.list().all()
        assert len(ranges) == 1
        r = ranges[0]
        assert r.name == "prod-range"
        assert r.start_vlan_id == 100

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(vlan_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_vlanrange_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlanrange/ZG5z:prod-range",
                        "name": "prod-range",
                        "vlan_view": "vlanview/ZG5z:default",
                        "start_vlan_id": 100,
                        "end_vlan_id": 200,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        ranges = await c.ipam.vlanrange.list(vlan_view="vlanview/ZG5z:default").all()
        assert len(ranges) == 1
        params = captured[0].url.params
        assert params.get("vlan_view") == "vlanview/ZG5z:default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_vlanrange_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "vlanrange/ZG5z:prod-range",
                "name": "prod-range",
                "vlan_view": "vlanview/ZG5z:default",
                "start_vlan_id": 100,
                "end_vlan_id": 200,
            }
        )

    async with _client(handler) as c:
        ref = "vlanrange/ZG5z:prod-range"
        r = await c.ipam.vlanrange.get(ref)
        assert r.name == "prod-range"
        assert r.end_vlan_id == 200
        assert r.vlan_view == "vlanview/ZG5z:default"


# ---------------------------------------------------------------------------
# 4. find_one(name="prod-range") - returns first match
# ---------------------------------------------------------------------------


async def test_vlanrange_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlanrange/ZG5z:prod-range",
                        "name": "prod-range",
                        "vlan_view": "vlanview/ZG5z:default",
                        "start_vlan_id": 100,
                        "end_vlan_id": 200,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.ipam.vlanrange.find_one(name="prod-range")
        assert r is not None
        assert r.name == "prod-range"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_vlanrange_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "vlanrange/ZG5z:dev-range",
                "name": "dev-range",
                "vlan_view": "vlanview/ZG5z:default",
                "start_vlan_id": 300,
                "end_vlan_id": 400,
            }
        )

    async with _client(handler) as c:
        r = await c.ipam.vlanrange.create(
            {
                "name": "dev-range",
                "vlan_view": "vlanview/ZG5z:default",
                "start_vlan_id": 300,
                "end_vlan_id": 400,
            }
        )
        assert r.name == "dev-range"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"dev-range"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (uuid)
# ---------------------------------------------------------------------------


async def test_vlanrange_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "vlanrange/ZG5z:prod-range",
                "name": "prod-range",
                "vlan_view": "vlanview/ZG5z:default",
                "start_vlan_id": 100,
                "end_vlan_id": 200,
            }
        )

    async with _client(handler) as c:
        ref = "vlanrange/ZG5z:prod-range"
        vr = Vlanrange(
            name="prod-range",
            comment="updated",
            uuid="some-uuid",  # RO
        )
        await c.ipam.vlanrange.update(ref, vr)
        body = json.loads(captured[0].content.decode())

        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("comment") == "updated"
