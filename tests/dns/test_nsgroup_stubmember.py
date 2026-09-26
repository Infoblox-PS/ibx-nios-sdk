# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupStubmemberResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.nsgroup_stubmember import NsgroupStubmember
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_nsgroup_stubmember_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "nsgroup:stubmember/ZG5z:stubgrp",
                        "name": "stubgrp",
                        "comment": "stub member group",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.nsgroup_stubmember.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "stubgrp"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


async def test_nsgroup_stubmember_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "nsgroup:stubmember/ZG5z:stubgrp",
                "name": "stubgrp",
                "comment": "stub group",
            }
        )

    async with _client(handler) as c:
        ref = "nsgroup:stubmember/ZG5z:stubgrp"
        g = await c.dns.nsgroup_stubmember.get(ref)
        assert g.name == "stubgrp"
        assert g.comment == "stub group"


async def test_nsgroup_stubmember_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [{"_ref": "nsgroup:stubmember/ZG5z:stubgrp", "name": "stubgrp"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.nsgroup_stubmember.find_one(name="stubgrp")
        assert g is not None
        assert g.name == "stubgrp"


async def test_nsgroup_stubmember_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:stubmember/NEW:stubgrp", "name": "stubgrp"})

    async with _client(handler) as c:
        g = await c.dns.nsgroup_stubmember.create({"name": "stubgrp", "comment": "new"})
        assert g.name == "stubgrp"
        body = captured[0].content.decode()
        assert '"name":"stubgrp"' in body
        assert '"comment":"new"' in body


async def test_nsgroup_stubmember_update_strips_readonly() -> None:
    """uuid is read-only; it must not appear in the PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:stubmember/ABC:stubgrp", "name": "stubgrp2"})

    async with _client(handler) as c:
        ref = "nsgroup:stubmember/ABC:stubgrp"
        g = NsgroupStubmember(name="stubgrp2", uuid="strip-me", comment="updated")
        await c.dns.nsgroup_stubmember.update(ref, g)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "readonly field must be stripped from update body"
        assert '"name":"stubgrp2"' in body


async def test_nsgroup_stubmember_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("nsgroup:stubmember/ABC:stubgrp")

    async with _client(handler) as c:
        result = await c.dns.nsgroup_stubmember.delete("nsgroup:stubmember/ABC:stubgrp")
        assert result == "nsgroup:stubmember/ABC:stubgrp"
