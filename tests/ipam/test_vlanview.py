# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VlanviewResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.vlanview import Vlanview
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns vlanview objects
# ---------------------------------------------------------------------------


async def test_vlanview_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlanview/ZG5z:default",
                        "name": "default",
                        "start_vlan_id": 1,
                        "end_vlan_id": 4094,
                        "comment": "Default VLAN view",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        views = await c.ipam.vlanview.list().all()
        assert len(views) == 1
        v = views[0]
        assert v.name == "default"
        assert v.start_vlan_id == 1

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_vlanview_list_by_name() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlanview/ZG5z:default",
                        "name": "default",
                        "start_vlan_id": 1,
                        "end_vlan_id": 4094,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        views = await c.ipam.vlanview.list(name="default").all()
        assert len(views) == 1
        params = captured[0].url.params
        assert params.get("name") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_vlanview_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "vlanview/ZG5z:default",
                "name": "default",
                "start_vlan_id": 1,
                "end_vlan_id": 4094,
                "comment": "Default VLAN view",
            }
        )

    async with _client(handler) as c:
        ref = "vlanview/ZG5z:default"
        v = await c.ipam.vlanview.get(ref)
        assert v.name == "default"
        assert v.end_vlan_id == 4094
        assert v.comment == "Default VLAN view"


# ---------------------------------------------------------------------------
# 4. find_one(name="default") - returns first match
# ---------------------------------------------------------------------------


async def test_vlanview_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlanview/ZG5z:default",
                        "name": "default",
                        "start_vlan_id": 1,
                        "end_vlan_id": 4094,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        v = await c.ipam.vlanview.find_one(name="default")
        assert v is not None
        assert v.name == "default"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_vlanview_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "vlanview/ZG5z:corp",
                "name": "corp",
                "start_vlan_id": 100,
                "end_vlan_id": 200,
                "comment": "Corp VLAN view",
            }
        )

    async with _client(handler) as c:
        v = await c.ipam.vlanview.create(
            {"name": "corp", "start_vlan_id": 100, "end_vlan_id": 200, "comment": "Corp VLAN view"}
        )
        assert v.name == "corp"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"corp"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (uuid)
# ---------------------------------------------------------------------------


async def test_vlanview_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "vlanview/ZG5z:default",
                "name": "default",
                "start_vlan_id": 1,
                "end_vlan_id": 4094,
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "vlanview/ZG5z:default"
        vv = Vlanview(
            name="default",
            comment="updated",
            uuid="some-uuid",  # RO
        )
        await c.ipam.vlanview.update(ref, vv)
        body = json.loads(captured[0].content.decode())

        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("comment") == "updated"
