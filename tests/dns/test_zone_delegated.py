# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneDelegatedResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.zone_delegated import ZoneDelegated
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


async def test_zone_delegated_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_delegated/ZG5z:sub.example.com/default",
                        "fqdn": "sub.example.com",
                        "view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        zones = await c.dns.zone_delegated.list(view="default").all()
        assert len(zones) == 1
        z = zones[0]
        assert z.fqdn == "sub.example.com"
        assert z.view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "fqdn" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with delegate_to
# ---------------------------------------------------------------------------


async def test_zone_delegated_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "zone_delegated/ZG5z:sub.example.com/default",
                "fqdn": "sub.example.com",
                "view": "default",
                "comment": "delegated zone",
                "delegate_to": [{"address": "10.0.0.1", "name": "ns1.child.example.com"}],
                "delegated_ttl": 300,
            }
        )

    async with _client(handler) as c:
        ref = "zone_delegated/ZG5z:sub.example.com/default"
        z = await c.dns.zone_delegated.get(ref)
        assert z.fqdn == "sub.example.com"
        assert z.view == "default"
        assert z.comment == "delegated zone"
        assert z.delegate_to is not None
        assert len(z.delegate_to) == 1
        assert z.delegate_to[0].address == "10.0.0.1"
        assert z.delegated_ttl == 300


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_zone_delegated_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_delegated/ZG5z:sub.example.com/default",
                        "fqdn": "sub.example.com",
                        "view": "default",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_delegated.find_one(fqdn="sub.example.com")
        assert z is not None
        assert z.fqdn == "sub.example.com"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_zone_delegated_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_delegated/NEW:sub.example.com/default",
                "fqdn": "sub.example.com",
                "view": "default",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_delegated.create(
            {
                "fqdn": "sub.example.com",
                "view": "default",
                "delegate_to": [{"address": "10.0.0.1", "name": "ns1.child.example.com"}],
            }
        )
        assert z.fqdn == "sub.example.com"
        body = captured[0].content.decode()
        assert '"fqdn":"sub.example.com"' in body
        assert '"view":"default"' in body
        assert '"delegate_to"' in body
        assert '"10.0.0.1"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_zone_delegated_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_delegated/ZG5z:sub.example.com/default",
                "fqdn": "sub.example.com",
                "view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "zone_delegated/ZG5z:sub.example.com/default"
        z = ZoneDelegated(
            fqdn="sub.example.com",
            view="default",
            comment="updated",
            address="10.0.0.1",  # RO
            dns_fqdn="sub.example.com.",  # RO
            locked_by="admin",  # RO
            parent="example.com",  # RO
            uuid="some-uuid",  # RO
            ms_managed="READ",  # RO
        )
        await c.dns.zone_delegated.update(ref, z)
        body = captured[0].content.decode()

        # Readonly fields must not appear
        assert '"address"' not in body, "address is readonly - must be stripped"
        assert '"dns_fqdn"' not in body, "dns_fqdn is readonly - must be stripped"
        assert '"locked_by"' not in body, "locked_by is readonly - must be stripped"
        assert '"parent"' not in body, "parent is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"ms_managed"' not in body, "ms_managed is readonly - must be stripped"

        # Writable fields must be present
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_zone_delegated_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("zone_delegated/ZG5z:sub.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.zone_delegated.delete("zone_delegated/ZG5z:sub.example.com/default")
        assert result == "zone_delegated/ZG5z:sub.example.com/default"
