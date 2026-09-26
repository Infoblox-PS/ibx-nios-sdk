# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneRpResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.zone_rp import ZoneRp
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


async def test_zone_rp_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_rp/ZG5z:rpz.example.com/default",
                        "fqdn": "rpz.example.com",
                        "view": "default",
                        "comment": "",
                        "disable": False,
                        "rpz_type": "LOCAL",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        zones = await c.dns.zone_rp.list(view="default").all()
        assert len(zones) == 1
        z = zones[0]
        assert z.fqdn == "rpz.example.com"
        assert z.view == "default"
        assert z.rpz_type == "LOCAL"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "fqdn" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with grid_primary
# ---------------------------------------------------------------------------


async def test_zone_rp_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "zone_rp/ZG5z:rpz.example.com/default",
                "fqdn": "rpz.example.com",
                "view": "default",
                "comment": "rpz zone",
                "rpz_policy": "PASSTHRU",
                "rpz_severity": "WARNING",
                "rpz_type": "LOCAL",
                "grid_primary": [
                    {
                        "name": "member1.infoblox.local",
                        "stealth": False,
                        "lead": True,
                    }
                ],
            }
        )

    async with _client(handler) as c:
        ref = "zone_rp/ZG5z:rpz.example.com/default"
        z = await c.dns.zone_rp.get(ref)
        assert z.fqdn == "rpz.example.com"
        assert z.view == "default"
        assert z.comment == "rpz zone"
        assert z.rpz_policy == "PASSTHRU"
        assert z.rpz_severity == "WARNING"
        assert z.rpz_type == "LOCAL"
        assert z.grid_primary is not None
        assert len(z.grid_primary) == 1
        assert z.grid_primary[0].name == "member1.infoblox.local"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_zone_rp_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_rp/ZG5z:rpz.example.com/default",
                        "fqdn": "rpz.example.com",
                        "view": "default",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_rp.find_one(fqdn="rpz.example.com")
        assert z is not None
        assert z.fqdn == "rpz.example.com"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_zone_rp_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_rp/NEW:rpz.example.com/default",
                "fqdn": "rpz.example.com",
                "view": "default",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_rp.create(
            {
                "fqdn": "rpz.example.com",
                "view": "default",
                "rpz_policy": "PASSTHRU",
                "grid_primary": [{"name": "member1.infoblox.local"}],
            }
        )
        assert z.fqdn == "rpz.example.com"
        body = captured[0].content.decode()
        assert '"fqdn":"rpz.example.com"' in body
        assert '"view":"default"' in body
        assert '"rpz_policy":"PASSTHRU"' in body
        assert '"grid_primary"' in body
        assert '"member1.infoblox.local"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_zone_rp_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_rp/ZG5z:rpz.example.com/default",
                "fqdn": "rpz.example.com",
                "view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "zone_rp/ZG5z:rpz.example.com/default"
        z = ZoneRp(
            fqdn="rpz.example.com",
            view="default",
            comment="updated",
            address="10.0.0.1",  # RO
            dns_soa_email="admin@example.com",  # RO
            locked_by="admin",  # RO
            parent="example.com",  # RO
            uuid="some-uuid",  # RO
            rpz_priority=1,  # RO
            rpz_last_updated_time=1234567890,  # RO
            primary_type="GRID",  # RO
            network_view="default",  # RO
        )
        await c.dns.zone_rp.update(ref, z)
        body = captured[0].content.decode()

        # Readonly fields must not appear
        assert '"address"' not in body, "address is readonly - must be stripped"
        assert '"dns_soa_email"' not in body, "dns_soa_email is readonly - must be stripped"
        assert '"locked_by"' not in body, "locked_by is readonly - must be stripped"
        assert '"parent"' not in body, "parent is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"rpz_priority"' not in body, "rpz_priority is readonly - must be stripped"
        assert '"rpz_last_updated_time"' not in body, (
            "rpz_last_updated_time is readonly - must be stripped"
        )
        assert '"primary_type"' not in body, "primary_type is readonly - must be stripped"
        assert '"network_view"' not in body, "network_view is readonly - must be stripped"

        # Writable fields must be present
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_zone_rp_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("zone_rp/ZG5z:rpz.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.zone_rp.delete("zone_rp/ZG5z:rpz.example.com/default")
        assert result == "zone_rp/ZG5z:rpz.example.com/default"
