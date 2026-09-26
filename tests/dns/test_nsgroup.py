# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.nsgroup import Nsgroup
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_nsgroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "nsgroup/ZG5z:default/true",
                        "name": "default",
                        "comment": "grid default",
                        "is_grid_default": True,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.nsgroup.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "default"
        assert g.is_grid_default is True

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


async def test_nsgroup_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "nsgroup/ZG5z:mygroup/false",
                "name": "mygroup",
                "comment": "test ns group",
                "is_grid_default": False,
            }
        )

    async with _client(handler) as c:
        ref = "nsgroup/ZG5z:mygroup/false"
        g = await c.dns.nsgroup.get(ref)
        assert g.name == "mygroup"
        assert g.comment == "test ns group"


async def test_nsgroup_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "nsgroup/ZG5z:mygroup/false",
                        "name": "mygroup",
                        "is_grid_default": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.nsgroup.find_one(name="mygroup")
        assert g is not None
        assert g.name == "mygroup"


async def test_nsgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": "nsgroup/NEW:mygroup/false", "name": "mygroup", "is_grid_default": False}
        )

    async with _client(handler) as c:
        g = await c.dns.nsgroup.create({"name": "mygroup", "comment": "new ns group"})
        assert g.name == "mygroup"
        body = captured[0].content.decode()
        assert '"name":"mygroup"' in body
        assert '"comment":"new ns group"' in body


async def test_nsgroup_update_strips_readonly() -> None:
    """uuid is read-only; it must not be sent in PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup/ABC:mygroup/false", "name": "mygroup2"})

    async with _client(handler) as c:
        ref = "nsgroup/ABC:mygroup/false"
        g = Nsgroup(name="mygroup2", uuid="should-be-stripped", comment="updated")
        await c.dns.nsgroup.update(ref, g)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "readonly field must be stripped from update body"
        assert '"name":"mygroup2"' in body


async def test_nsgroup_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("nsgroup/ABC:mygroup/false")

    async with _client(handler) as c:
        result = await c.dns.nsgroup.delete("nsgroup/ABC:mygroup/false")
        assert result == "nsgroup/ABC:mygroup/false"
