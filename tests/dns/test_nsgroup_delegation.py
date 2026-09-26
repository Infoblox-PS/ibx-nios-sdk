# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupDelegationResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.nsgroup_delegation import NsgroupDelegation
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_nsgroup_delegation_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "nsgroup:delegation/ZG5z:deleggrp",
                        "name": "deleggrp",
                        "comment": "delegation group",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.nsgroup_delegation.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "deleggrp"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


async def test_nsgroup_delegation_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "nsgroup:delegation/ZG5z:deleggrp",
                "name": "deleggrp",
                "comment": "delegation group",
            }
        )

    async with _client(handler) as c:
        ref = "nsgroup:delegation/ZG5z:deleggrp"
        g = await c.dns.nsgroup_delegation.get(ref)
        assert g.name == "deleggrp"
        assert g.comment == "delegation group"


async def test_nsgroup_delegation_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [{"_ref": "nsgroup:delegation/ZG5z:deleggrp", "name": "deleggrp"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.nsgroup_delegation.find_one(name="deleggrp")
        assert g is not None
        assert g.name == "deleggrp"


async def test_nsgroup_delegation_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:delegation/NEW:deleggrp", "name": "deleggrp"})

    async with _client(handler) as c:
        g = await c.dns.nsgroup_delegation.create({"name": "deleggrp", "comment": "new"})
        assert g.name == "deleggrp"
        body = captured[0].content.decode()
        assert '"name":"deleggrp"' in body
        assert '"comment":"new"' in body


async def test_nsgroup_delegation_update_strips_readonly() -> None:
    """uuid is read-only; it must not appear in the PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:delegation/ABC:deleggrp", "name": "deleggrp2"})

    async with _client(handler) as c:
        ref = "nsgroup:delegation/ABC:deleggrp"
        g = NsgroupDelegation(name="deleggrp2", uuid="strip-me", comment="updated")
        await c.dns.nsgroup_delegation.update(ref, g)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "readonly field must be stripped from update body"
        assert '"name":"deleggrp2"' in body


async def test_nsgroup_delegation_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("nsgroup:delegation/ABC:deleggrp")

    async with _client(handler) as c:
        result = await c.dns.nsgroup_delegation.delete("nsgroup:delegation/ABC:deleggrp")
        assert result == "nsgroup:delegation/ABC:deleggrp"
