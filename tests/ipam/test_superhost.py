# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SuperhostResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.superhost import Superhost
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns superhost objects
# ---------------------------------------------------------------------------


async def test_superhost_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "superhost/ZG5z:sh1",
                        "name": "myhost.example.com",
                        "comment": "Primary superhost",
                        "dhcp_associated_objects": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        hosts = await c.ipam.superhost.list().all()
        assert len(hosts) == 1
        h = hosts[0]
        assert h.name == "myhost.example.com"
        assert h.comment == "Primary superhost"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name="myhost.example.com") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_superhost_list_by_name() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "superhost/ZG5z:sh1",
                        "name": "myhost.example.com",
                        "comment": "",
                        "dhcp_associated_objects": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        hosts = await c.ipam.superhost.list(name="myhost.example.com").all()
        assert len(hosts) == 1
        params = captured[0].url.params
        assert params.get("name") == "myhost.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_superhost_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "superhost/ZG5z:sh1",
                "name": "myhost.example.com",
                "comment": "Primary superhost",
                "dhcp_associated_objects": ["fixedaddress/ZG5z:1"],
            }
        )

    async with _client(handler) as c:
        ref = "superhost/ZG5z:sh1"
        h = await c.ipam.superhost.get(ref)
        assert h.name == "myhost.example.com"
        assert h.dhcp_associated_objects == ["fixedaddress/ZG5z:1"]


# ---------------------------------------------------------------------------
# 4. find_one(name="myhost.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_superhost_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "superhost/ZG5z:sh1",
                        "name": "myhost.example.com",
                        "comment": "",
                        "dhcp_associated_objects": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        h = await c.ipam.superhost.find_one(name="myhost.example.com")
        assert h is not None
        assert h.name == "myhost.example.com"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_superhost_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "superhost/ZG5z:sh2",
                "name": "newhost.example.com",
                "comment": "New superhost",
                "dhcp_associated_objects": [],
            }
        )

    async with _client(handler) as c:
        h = await c.ipam.superhost.create(
            {"name": "newhost.example.com", "comment": "New superhost"}
        )
        assert h.name == "newhost.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"newhost.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (uuid)
# ---------------------------------------------------------------------------


async def test_superhost_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "superhost/ZG5z:sh1",
                "name": "myhost.example.com",
                "comment": "updated",
                "dhcp_associated_objects": [],
            }
        )

    async with _client(handler) as c:
        ref = "superhost/ZG5z:sh1"
        sh = Superhost(
            name="myhost.example.com",
            comment="updated",
            uuid="some-uuid",  # RO
        )
        await c.ipam.superhost.update(ref, sh)
        body = json.loads(captured[0].content.decode())

        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("comment") == "updated"
