# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneStubResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.zone_stub import ZoneStub
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


async def test_zone_stub_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_stub/ZG5z:stub.example.com/default",
                        "fqdn": "stub.example.com",
                        "view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        zones = await c.dns.zone_stub.list(view="default").all()
        assert len(zones) == 1
        z = zones[0]
        assert z.fqdn == "stub.example.com"
        assert z.view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "fqdn" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model with stub_from
# ---------------------------------------------------------------------------


async def test_zone_stub_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "zone_stub/ZG5z:stub.example.com/default",
                "fqdn": "stub.example.com",
                "view": "default",
                "comment": "stub zone",
                "stub_from": [{"address": "10.0.0.1", "name": "ns1.example.com"}],
            }
        )

    async with _client(handler) as c:
        ref = "zone_stub/ZG5z:stub.example.com/default"
        z = await c.dns.zone_stub.get(ref)
        assert z.fqdn == "stub.example.com"
        assert z.view == "default"
        assert z.comment == "stub zone"
        assert z.stub_from is not None
        assert len(z.stub_from) == 1
        assert z.stub_from[0].address == "10.0.0.1"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_zone_stub_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_stub/ZG5z:stub.example.com/default",
                        "fqdn": "stub.example.com",
                        "view": "default",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_stub.find_one(fqdn="stub.example.com")
        assert z is not None
        assert z.fqdn == "stub.example.com"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_zone_stub_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_stub/NEW:stub.example.com/default",
                "fqdn": "stub.example.com",
                "view": "default",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_stub.create(
            {
                "fqdn": "stub.example.com",
                "view": "default",
                "stub_from": [{"address": "10.0.0.1", "name": "ns1.example.com"}],
            }
        )
        assert z.fqdn == "stub.example.com"
        body = captured[0].content.decode()
        assert '"fqdn":"stub.example.com"' in body
        assert '"view":"default"' in body
        assert '"stub_from"' in body
        assert '"10.0.0.1"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_zone_stub_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_stub/ZG5z:stub.example.com/default",
                "fqdn": "stub.example.com",
                "view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "zone_stub/ZG5z:stub.example.com/default"
        z = ZoneStub(
            fqdn="stub.example.com",
            view="default",
            comment="updated",
            address="10.0.0.1",  # RO
            dns_fqdn="stub.example.com.",  # RO
            locked_by="admin",  # RO
            parent="example.com",  # RO
            uuid="some-uuid",  # RO
            soa_email="admin@example.com",  # RO
            soa_serial_number=2024010101,  # RO
        )
        await c.dns.zone_stub.update(ref, z)
        body = captured[0].content.decode()

        # Readonly fields must not appear
        assert '"address"' not in body, "address is readonly - must be stripped"
        assert '"dns_fqdn"' not in body, "dns_fqdn is readonly - must be stripped"
        assert '"locked_by"' not in body, "locked_by is readonly - must be stripped"
        assert '"parent"' not in body, "parent is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"soa_email"' not in body, "soa_email is readonly - must be stripped"
        assert '"soa_serial_number"' not in body, (
            "soa_serial_number is readonly - must be stripped"
        )

        # Writable fields must be present
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_zone_stub_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("zone_stub/ZG5z:stub.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.zone_stub.delete("zone_stub/ZG5z:stub.example.com/default")
        assert result == "zone_stub/ZG5z:stub.example.com/default"
