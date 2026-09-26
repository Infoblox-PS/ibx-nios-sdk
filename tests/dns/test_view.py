# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ViewResource - CRUD, find_one, list, pagination."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.view import View
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_view_list_default_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "view/ZG5zLnZpZXck:default/true",
                        "name": "default",
                        "is_default": True,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        views = await c.dns.view.list().all()
        assert len(views) == 1
        v = views[0]
        assert v.name == "default"
        assert v.is_default is True

        # verify WAPI params
        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


async def test_view_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "view/ABC:custom/false",
                "name": "custom",
                "is_default": False,
                "comment": "test view",
            }
        )

    async with _client(handler) as c:
        ref = "view/ABC:custom/false"
        v = await c.dns.view.get(ref)
        assert v.name == "custom"
        assert v.comment == "test view"


async def test_view_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [{"_ref": "view/X:custom/false", "name": "custom", "is_default": False}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        v = await c.dns.view.find_one(name="custom")
        assert v is not None
        assert v.name == "custom"


async def test_view_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": "view/NEW:custom/false", "name": "custom", "is_default": False}
        )

    async with _client(handler) as c:
        v = await c.dns.view.create({"name": "custom", "comment": "new view"})
        assert v.name == "custom"
        body = captured[0].content.decode()
        assert '"name":"custom"' in body
        assert '"comment":"new view"' in body


async def test_view_update_strips_readonly() -> None:
    """is_default is read-only in the swagger; it must not be PUT."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "view/ABC:custom/false", "name": "custom2"})

    async with _client(handler) as c:
        ref = "view/ABC:custom/false"
        v = View(name="custom2", is_default=True, comment="renamed")
        await c.dns.view.update(ref, v)
        body = captured[0].content.decode()
        assert '"is_default"' not in body, "readonly field must be stripped from update body"
        assert '"name":"custom2"' in body


async def test_view_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("view/ABC:custom/false")

    async with _client(handler) as c:
        result = await c.dns.view.delete("view/ABC:custom/false")
        assert result == "view/ABC:custom/false"
