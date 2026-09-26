# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupForwardstubserverResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.nsgroup_forwardstubserver import NsgroupForwardstubserver
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_nsgroup_forwardstubserver_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "nsgroup:forwardstubserver/ZG5z:fssgrp",
                        "name": "fssgrp",
                        "comment": "forward stub server group",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.nsgroup_forwardstubserver.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "fssgrp"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


async def test_nsgroup_forwardstubserver_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "nsgroup:forwardstubserver/ZG5z:fssgrp",
                "name": "fssgrp",
                "comment": "forward stub group",
            }
        )

    async with _client(handler) as c:
        ref = "nsgroup:forwardstubserver/ZG5z:fssgrp"
        g = await c.dns.nsgroup_forwardstubserver.get(ref)
        assert g.name == "fssgrp"
        assert g.comment == "forward stub group"


async def test_nsgroup_forwardstubserver_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [{"_ref": "nsgroup:forwardstubserver/ZG5z:fssgrp", "name": "fssgrp"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.nsgroup_forwardstubserver.find_one(name="fssgrp")
        assert g is not None
        assert g.name == "fssgrp"


async def test_nsgroup_forwardstubserver_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:forwardstubserver/NEW:fssgrp", "name": "fssgrp"})

    async with _client(handler) as c:
        g = await c.dns.nsgroup_forwardstubserver.create({"name": "fssgrp", "comment": "new"})
        assert g.name == "fssgrp"
        body = captured[0].content.decode()
        assert '"name":"fssgrp"' in body
        assert '"comment":"new"' in body


async def test_nsgroup_forwardstubserver_update_strips_readonly() -> None:
    """uuid is read-only; it must not appear in the PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:forwardstubserver/ABC:fssgrp", "name": "fssgrp2"})

    async with _client(handler) as c:
        ref = "nsgroup:forwardstubserver/ABC:fssgrp"
        g = NsgroupForwardstubserver(name="fssgrp2", uuid="strip-me", comment="updated")
        await c.dns.nsgroup_forwardstubserver.update(ref, g)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "readonly field must be stripped from update body"
        assert '"name":"fssgrp2"' in body


async def test_nsgroup_forwardstubserver_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("nsgroup:forwardstubserver/ABC:fssgrp")

    async with _client(handler) as c:
        result = await c.dns.nsgroup_forwardstubserver.delete(
            "nsgroup:forwardstubserver/ABC:fssgrp"
        )
        assert result == "nsgroup:forwardstubserver/ABC:fssgrp"
