# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NsgroupForwardingmemberResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.nsgroup_forwardingmember import NsgroupForwardingmember
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_nsgroup_forwardingmember_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "nsgroup:forwardingmember/ZG5z:fwdgrp",
                        "name": "fwdgrp",
                        "comment": "forwarding member group",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.nsgroup_forwardingmember.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "fwdgrp"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


async def test_nsgroup_forwardingmember_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "nsgroup:forwardingmember/ZG5z:fwdgrp",
                "name": "fwdgrp",
                "comment": "forwarding group",
            }
        )

    async with _client(handler) as c:
        ref = "nsgroup:forwardingmember/ZG5z:fwdgrp"
        g = await c.dns.nsgroup_forwardingmember.get(ref)
        assert g.name == "fwdgrp"
        assert g.comment == "forwarding group"


async def test_nsgroup_forwardingmember_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [{"_ref": "nsgroup:forwardingmember/ZG5z:fwdgrp", "name": "fwdgrp"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.nsgroup_forwardingmember.find_one(name="fwdgrp")
        assert g is not None
        assert g.name == "fwdgrp"


async def test_nsgroup_forwardingmember_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:forwardingmember/NEW:fwdgrp", "name": "fwdgrp"})

    async with _client(handler) as c:
        g = await c.dns.nsgroup_forwardingmember.create({"name": "fwdgrp", "comment": "new"})
        assert g.name == "fwdgrp"
        body = captured[0].content.decode()
        assert '"name":"fwdgrp"' in body
        assert '"comment":"new"' in body


async def test_nsgroup_forwardingmember_update_strips_readonly() -> None:
    """uuid is read-only; it must not appear in the PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "nsgroup:forwardingmember/ABC:fwdgrp", "name": "fwdgrp2"})

    async with _client(handler) as c:
        ref = "nsgroup:forwardingmember/ABC:fwdgrp"
        g = NsgroupForwardingmember(name="fwdgrp2", uuid="strip-me", comment="updated")
        await c.dns.nsgroup_forwardingmember.update(ref, g)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "readonly field must be stripped from update body"
        assert '"name":"fwdgrp2"' in body


async def test_nsgroup_forwardingmember_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("nsgroup:forwardingmember/ABC:fwdgrp")

    async with _client(handler) as c:
        result = await c.dns.nsgroup_forwardingmember.delete("nsgroup:forwardingmember/ABC:fwdgrp")
        assert result == "nsgroup:forwardingmember/ABC:fwdgrp"
