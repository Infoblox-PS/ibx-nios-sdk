# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneForwardResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.zone_forward import ZoneForward
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


async def test_zone_forward_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_forward/ZG5z:example.com/default",
                        "fqdn": "example.com",
                        "view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        zones = await c.dns.zone_forward.list(view="default").all()
        assert len(zones) == 1
        z = zones[0]
        assert z.fqdn == "example.com"
        assert z.view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "fqdn" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with forward_to
# ---------------------------------------------------------------------------


async def test_zone_forward_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "zone_forward/ZG5z:example.com/default",
                "fqdn": "example.com",
                "view": "default",
                "comment": "fwd zone",
                "forward_to": [{"address": "1.2.3.4", "name": "ns1.example.com"}],
            }
        )

    async with _client(handler) as c:
        ref = "zone_forward/ZG5z:example.com/default"
        z = await c.dns.zone_forward.get(ref)
        assert z.fqdn == "example.com"
        assert z.view == "default"
        assert z.comment == "fwd zone"
        assert z.forward_to is not None
        assert len(z.forward_to) == 1
        assert z.forward_to[0].address == "1.2.3.4"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_zone_forward_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_forward/ZG5z:example.com/default",
                        "fqdn": "example.com",
                        "view": "default",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_forward.find_one(fqdn="example.com")
        assert z is not None
        assert z.fqdn == "example.com"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_zone_forward_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_forward/NEW:example.com/default",
                "fqdn": "example.com",
                "view": "default",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_forward.create(
            {
                "fqdn": "example.com",
                "view": "default",
                "forward_to": [{"address": "1.2.3.4", "name": "ns1.example.com"}],
            }
        )
        assert z.fqdn == "example.com"
        body = captured[0].content.decode()
        assert '"fqdn":"example.com"' in body
        assert '"view":"default"' in body
        assert '"forward_to"' in body
        assert '"1.2.3.4"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_zone_forward_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_forward/ZG5z:example.com/default",
                "fqdn": "example.com",
                "view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "zone_forward/ZG5z:example.com/default"
        z = ZoneForward(
            fqdn="example.com",
            view="default",
            comment="updated",
            address="1.2.3.4",  # RO
            dns_fqdn="example.com.",  # RO
            locked_by="admin",  # RO
            parent="parent_zone",  # RO
            uuid="some-uuid",  # RO
            ms_managed="READ",  # RO
        )
        await c.dns.zone_forward.update(ref, z)
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


async def test_zone_forward_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("zone_forward/ZG5z:example.com/default")

    async with _client(handler) as c:
        result = await c.dns.zone_forward.delete("zone_forward/ZG5z:example.com/default")
        assert result == "zone_forward/ZG5z:example.com/default"
