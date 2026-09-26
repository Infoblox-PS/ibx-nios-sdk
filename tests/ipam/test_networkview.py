# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkviewResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.networkview import Networkview
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns networkview objects
# ---------------------------------------------------------------------------


async def test_networkview_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "networkview/ZG5z:default",
                        "name": "default",
                        "is_default": True,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        views = await c.ipam.networkview.list().all()
        assert len(views) == 1
        v = views[0]
        assert v.name == "default"
        assert v.is_default is True

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name__like="corp") - filter translated correctly
# ---------------------------------------------------------------------------


async def test_networkview_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "networkview/ZG5z:corporate",
                        "name": "corporate",
                        "is_default": False,
                        "comment": "Corp view",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        views = await c.ipam.networkview.list(name__like="corp").all()
        assert len(views) == 1
        assert views[0].name == "corporate"

        params = captured[0].url.params
        assert any("corp" in v for v in params.values())


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_networkview_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "networkview/ZG5z:default",
                "name": "default",
                "is_default": True,
                "comment": "Default network view",
            }
        )

    async with _client(handler) as c:
        ref = "networkview/ZG5z:default"
        v = await c.ipam.networkview.get(ref)
        assert v.name == "default"
        assert v.is_default is True
        assert v.comment == "Default network view"


# ---------------------------------------------------------------------------
# 4. find_one(name="default") - returns first match
# ---------------------------------------------------------------------------


async def test_networkview_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "networkview/ZG5z:default",
                        "name": "default",
                        "is_default": True,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        v = await c.ipam.networkview.find_one(name="default")
        assert v is not None
        assert v.name == "default"
        assert v.is_default is True


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_networkview_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "networkview/ZG5z:corpview",
                "name": "corpview",
                "is_default": False,
                "comment": "Corporate view",
            }
        )

    async with _client(handler) as c:
        v = await c.ipam.networkview.create({"name": "corpview", "comment": "Corporate view"})
        assert v.name == "corpview"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"corpview"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {...}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_networkview_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "networkview/ZG5z:default",
                "name": "default",
                "is_default": True,
                "comment": "Updated comment",
            }
        )

    async with _client(handler) as c:
        ref = "networkview/ZG5z:default"
        v = await c.ipam.networkview.update(ref, {"comment": "Updated comment"})
        assert v.comment == "Updated comment"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path
        body = req.content.decode()
        assert '"comment":"Updated comment"' in body


# ---------------------------------------------------------------------------
# Extra: readonly-strip on update (is_default, uuid are RO)
# ---------------------------------------------------------------------------


async def test_networkview_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "networkview/ZG5z:default",
                "name": "default",
                "is_default": True,
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "networkview/ZG5z:default"
        nv = Networkview(
            name="default",
            comment="updated",
            is_default=True,  # RO
            uuid="some-uuid",  # RO
        )
        await c.ipam.networkview.update(ref, nv)
        body = json.loads(captured[0].content.decode())

        # Readonly fields must NOT appear
        assert "is_default" not in body, "is_default is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"

        # Writable fields must appear
        assert body["name"] == "default"
        assert body["comment"] == "updated"
