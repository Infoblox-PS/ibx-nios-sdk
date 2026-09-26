# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SuperhostchildResource - list, get, find_one (all fields are readonly on write)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns superhostchild objects
# ---------------------------------------------------------------------------


async def test_superhostchild_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "superhostchild/ZG5z:shc1",
                        "name": "child1.example.com",
                        "record_parent": "superhost/ZG5z:sh1",
                        "parent": "superhost/ZG5z:sh1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        children = await c.ipam.superhostchild.list().all()
        assert len(children) == 1
        c2 = children[0]
        assert c2.name == "child1.example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(record_parent="superhost/ZG5z:sh1") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_superhostchild_list_by_parent() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "superhostchild/ZG5z:shc1",
                        "name": "child1.example.com",
                        "record_parent": "superhost/ZG5z:sh1",
                        "parent": "superhost/ZG5z:sh1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        children = await c.ipam.superhostchild.list(record_parent="superhost/ZG5z:sh1").all()
        assert len(children) == 1
        params = captured[0].url.params
        assert params.get("record_parent") == "superhost/ZG5z:sh1"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_superhostchild_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "superhostchild/ZG5z:shc1",
                "name": "child1.example.com",
                "record_parent": "superhost/ZG5z:sh1",
                "parent": "superhost/ZG5z:sh1",
                "type": "A",
            }
        )

    async with _client(handler) as c:
        ref = "superhostchild/ZG5z:shc1"
        child = await c.ipam.superhostchild.get(ref)
        assert child.name == "child1.example.com"
        assert child.type == "A"


# ---------------------------------------------------------------------------
# 4. find_one(name="child1.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_superhostchild_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "superhostchild/ZG5z:shc1",
                        "name": "child1.example.com",
                        "record_parent": "superhost/ZG5z:sh1",
                        "parent": "superhost/ZG5z:sh1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        child = await c.ipam.superhostchild.find_one(name="child1.example.com")
        assert child is not None
        assert child.name == "child1.example.com"


# ---------------------------------------------------------------------------
# 5. _wapi_type is "superhostchild"
# ---------------------------------------------------------------------------


async def test_superhostchild_wapi_type() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    async with _client(handler) as c:
        resource = c.ipam.superhostchild
        assert resource._wapi_type == "superhostchild"


# ---------------------------------------------------------------------------
# 6. model captures all readonly fields
# ---------------------------------------------------------------------------


async def test_superhostchild_model_fields() -> None:
    from ibx_nios_sdk.ipam.models.superhostchild import Superhostchild

    child = Superhostchild(
        name="child1.example.com",
        record_parent="superhost/ZG5z:sh1",
        parent="superhost/ZG5z:sh1",
        type="A",
        data="10.0.0.1",
    )
    assert child.name == "child1.example.com"
    assert child.data == "10.0.0.1"
    assert child.type == "A"
