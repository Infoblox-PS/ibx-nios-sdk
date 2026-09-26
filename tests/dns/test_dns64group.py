# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dns64groupResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.dns64group import Dns64group
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list with filter
# ---------------------------------------------------------------------------


async def test_dns64group_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "dns64group/ZG5z:mygroup",
                        "name": "mygroup",
                        "enable": True,
                        "comment": "DNS64 for IPv6 clients",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.dns64group.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "mygroup"
        assert g.comment == "DNS64 for IPv6 clients"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with nested ACL entries
# ---------------------------------------------------------------------------


async def test_dns64group_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "dns64group/ZG5z:mygroup",
                "name": "mygroup",
                "comment": "DNS64 group",
                "disable": False,
                "enable_dnssec_dns64": True,
                "prefix": "64:ff9b::/96",
                "clients": [{"address": "192.168.1.0/24", "permission": "ALLOW"}],
                "exclude": [{"address": "10.0.0.0/8", "permission": "DENY"}],
                "mapped": [{"address": "0.0.0.0/0", "permission": "ALLOW"}],
            }
        )

    async with _client(handler) as c:
        ref = "dns64group/ZG5z:mygroup"
        g = await c.dns.dns64group.get(ref)
        assert g.name == "mygroup"
        assert g.comment == "DNS64 group"
        assert g.disable is False
        assert g.enable_dnssec_dns64 is True
        assert g.prefix == "64:ff9b::/96"
        assert g.clients is not None
        assert len(g.clients) == 1
        assert g.clients[0].address == "192.168.1.0/24"
        assert g.clients[0].permission == "ALLOW"
        assert g.exclude is not None
        assert g.exclude[0].address == "10.0.0.0/8"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_dns64group_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "dns64group/ZG5z:mygroup",
                        "name": "mygroup",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.dns64group.find_one(name="mygroup")
        assert g is not None
        assert g.name == "mygroup"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_dns64group_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "dns64group/ZG5z:newgroup",
                "name": "newgroup",
                "comment": "new",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.dns64group.create(
            {
                "name": "newgroup",
                "comment": "new",
                "prefix": "64:ff9b::/96",
                "clients": [{"address": "0.0.0.0/0", "permission": "ALLOW"}],
            }
        )
        assert g.name == "newgroup"
        body = captured[0].content.decode()
        assert '"name":"newgroup"' in body
        assert '"prefix"' in body
        assert '"clients"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_dns64group_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "dns64group/ZG5z:mygroup",
                "name": "mygroup",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "dns64group/ZG5z:mygroup"
        g = Dns64group(
            name="mygroup",
            comment="updated",
            uuid="some-uuid",  # RO
        )
        await c.dns.dns64group.update(ref, g)
        body = captured[0].content.decode()
        # Readonly field must not appear
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        # Writable fields must be present
        assert '"name":"mygroup"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_dns64group_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("dns64group/ZG5z:mygroup")

    async with _client(handler) as c:
        result = await c.dns.dns64group.delete("dns64group/ZG5z:mygroup")
        assert result == "dns64group/ZG5z:mygroup"
