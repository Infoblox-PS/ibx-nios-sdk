# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DdnsPrincipalclusterResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.ddns_principalcluster import DdnsPrincipalcluster
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


async def test_ddns_principalcluster_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ddns:principalcluster/ZG5z:cluster1",
                        "name": "cluster1",
                        "comment": "primary cluster",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        clusters = await c.dns.ddns_principalcluster.list().all()
        assert len(clusters) == 1
        cl = clusters[0]
        assert cl.name == "cluster1"
        assert cl.comment == "primary cluster"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with principals
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ddns:principalcluster/ZG5z:cluster1",
                "name": "cluster1",
                "comment": "cluster comment",
                "group": "ddns:principalcluster:group/ZG5z:grp1",
                "principals": ["host/krb5.example.com", "dns/ns1.example.com"],
            }
        )

    async with _client(handler) as c:
        ref = "ddns:principalcluster/ZG5z:cluster1"
        cl = await c.dns.ddns_principalcluster.get(ref)
        assert cl.name == "cluster1"
        assert cl.comment == "cluster comment"
        assert cl.group == "ddns:principalcluster:group/ZG5z:grp1"
        assert cl.principals is not None
        assert len(cl.principals) == 2
        assert "host/krb5.example.com" in cl.principals


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ddns:principalcluster/ZG5z:cluster1",
                        "name": "cluster1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        cl = await c.dns.ddns_principalcluster.find_one(name="cluster1")
        assert cl is not None
        assert cl.name == "cluster1"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ddns:principalcluster/ZG5z:newcluster",
                "name": "newcluster",
                "comment": "new",
            }
        )

    async with _client(handler) as c:
        cl = await c.dns.ddns_principalcluster.create(
            {
                "name": "newcluster",
                "comment": "new",
                "principals": ["host/krb5.example.com"],
            }
        )
        assert cl.name == "newcluster"
        body = captured[0].content.decode()
        assert '"name":"newcluster"' in body
        assert '"principals"' in body
        assert "krb5.example.com" in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ddns:principalcluster/ZG5z:cluster1",
                "name": "cluster1",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "ddns:principalcluster/ZG5z:cluster1"
        cl = DdnsPrincipalcluster(
            name="cluster1",
            comment="updated",
            uuid="some-uuid",  # RO
        )
        await c.dns.ddns_principalcluster.update(ref, cl)
        body = captured[0].content.decode()
        # Readonly field must not appear
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        # Writable fields must be present
        assert '"name":"cluster1"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_ddns_principalcluster_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("ddns:principalcluster/ZG5z:cluster1")

    async with _client(handler) as c:
        result = await c.dns.ddns_principalcluster.delete("ddns:principalcluster/ZG5z:cluster1")
        assert result == "ddns:principalcluster/ZG5z:cluster1"
