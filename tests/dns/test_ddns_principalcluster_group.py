# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DdnsPrincipalclusterGroupResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.ddns_principalcluster_group import DdnsPrincipalclusterGroup
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_group_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ddns:principalcluster:group/ZG5z:grp1",
                        "name": "grp1",
                        "comment": "group one",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.ddns_principalcluster_group.list().all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "grp1"
        assert g.comment == "group one"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with clusters (RO)
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_group_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ddns:principalcluster:group/ZG5z:grp1",
                "name": "grp1",
                "comment": "group comment",
                "clusters": [
                    "ddns:principalcluster/ZG5z:c1",
                    "ddns:principalcluster/ZG5z:c2",
                ],
            }
        )

    async with _client(handler) as c:
        ref = "ddns:principalcluster:group/ZG5z:grp1"
        g = await c.dns.ddns_principalcluster_group.get(ref)
        assert g.name == "grp1"
        assert g.comment == "group comment"
        assert g.clusters is not None
        assert len(g.clusters) == 2
        assert "ddns:principalcluster/ZG5z:c1" in g.clusters


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_group_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ddns:principalcluster:group/ZG5z:grp1",
                        "name": "grp1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.ddns_principalcluster_group.find_one(name="grp1")
        assert g is not None
        assert g.name == "grp1"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_group_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ddns:principalcluster:group/ZG5z:newgrp",
                "name": "newgrp",
                "comment": "new group",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.ddns_principalcluster_group.create(
            {"name": "newgrp", "comment": "new group"}
        )
        assert g.name == "newgrp"
        body = captured[0].content.decode()
        assert '"name":"newgrp"' in body
        assert '"comment":"new group"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_group_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ddns:principalcluster:group/ZG5z:grp1",
                "name": "grp1",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "ddns:principalcluster:group/ZG5z:grp1"
        g = DdnsPrincipalclusterGroup(
            name="grp1",
            comment="updated",
            clusters=["ddns:principalcluster/ZG5z:c1"],  # RO
            uuid="some-uuid",  # RO
        )
        await c.dns.ddns_principalcluster_group.update(ref, g)
        body = captured[0].content.decode()
        # Readonly fields must not appear
        assert '"clusters"' not in body, "clusters is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        # Writable fields must be present
        assert '"name":"grp1"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_group_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("ddns:principalcluster:group/ZG5z:grp1")

    async with _client(handler) as c:
        result = await c.dns.ddns_principalcluster_group.delete(
            "ddns:principalcluster:group/ZG5z:grp1"
        )
        assert result == "ddns:principalcluster:group/ZG5z:grp1"
