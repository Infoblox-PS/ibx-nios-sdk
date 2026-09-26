# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VlanResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.vlan import Vlan
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns vlan objects
# ---------------------------------------------------------------------------


async def test_vlan_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlan/ZG5z:100",
                        "id": 100,
                        "name": "prod",
                        "parent": "vlanview/ZG5z:default",
                        "comment": "Production VLAN",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        vlans = await c.ipam.vlan.list().all()
        assert len(vlans) == 1
        v = vlans[0]
        assert v.id == 100
        assert v.name == "prod"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "id" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name="prod") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_vlan_list_by_name() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlan/ZG5z:100",
                        "id": 100,
                        "name": "prod",
                        "parent": "vlanview/ZG5z:default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        vlans = await c.ipam.vlan.list(name="prod").all()
        assert len(vlans) == 1
        params = captured[0].url.params
        assert params.get("name") == "prod"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_vlan_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "vlan/ZG5z:100",
                "id": 100,
                "name": "prod",
                "parent": "vlanview/ZG5z:default",
                "comment": "Production VLAN",
            }
        )

    async with _client(handler) as c:
        ref = "vlan/ZG5z:100"
        v = await c.ipam.vlan.get(ref)
        assert v.id == 100
        assert v.name == "prod"
        assert v.comment == "Production VLAN"


# ---------------------------------------------------------------------------
# 4. find_one(name="prod") - returns first match
# ---------------------------------------------------------------------------


async def test_vlan_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "vlan/ZG5z:100",
                        "id": 100,
                        "name": "prod",
                        "parent": "vlanview/ZG5z:default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        v = await c.ipam.vlan.find_one(name="prod")
        assert v is not None
        assert v.name == "prod"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_vlan_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "vlan/ZG5z:200",
                "id": 200,
                "name": "dev",
                "parent": "vlanview/ZG5z:default",
                "comment": "Dev VLAN",
            }
        )

    async with _client(handler) as c:
        v = await c.ipam.vlan.create(
            {"id": 200, "name": "dev", "parent": "vlanview/ZG5z:default", "comment": "Dev VLAN"}
        )
        assert v.id == 200

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"dev"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (assigned_to, status, uuid)
# ---------------------------------------------------------------------------


async def test_vlan_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "vlan/ZG5z:100",
                "id": 100,
                "name": "prod",
                "parent": "vlanview/ZG5z:default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "vlan/ZG5z:100"
        vlan = Vlan(
            name="prod",
            comment="updated",
            status="USED",  # RO
            uuid="some-uuid",  # RO
        )
        await c.ipam.vlan.update(ref, vlan)
        body = json.loads(captured[0].content.decode())

        assert "status" not in body, "status is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("comment") == "updated"
