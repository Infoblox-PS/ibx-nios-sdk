# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDhcidResource - read-only record list, get, find_one (no create/update)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_dhcid import RecordDhcid
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(zone="example.com")
# ---------------------------------------------------------------------------


async def test_record_dhcid_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:dhcid/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_dhcid.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="host")
# ---------------------------------------------------------------------------


async def test_record_dhcid_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:dhcid/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_dhcid.list(name__like="host").all()
        assert len(records) == 1
        assert records[0].name == "host.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_dhcid_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:dhcid/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "dhcid": "AAIBY...",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_dhcid.get("record:dhcid/ZG5z:host.example.com/default")
        assert r.name == "host.example.com"
        assert r.dhcid == "AAIBY..."


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_dhcid_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:dhcid/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_dhcid.find_one(name="host.example.com")
        assert r is not None
        assert r.name == "host.example.com"


# ---------------------------------------------------------------------------
# 5. Model - all fields RO (model roundtrip)
# ---------------------------------------------------------------------------


async def test_record_dhcid_model_roundtrip() -> None:
    """DHCID records are fully read-only; model accepts all fields."""
    r = RecordDhcid(
        **{
            "_ref": "record:dhcid/ZG5z:host.example.com/default",
            "name": "host.example.com",
            "dhcid": "AAIBY...",
            "creation_time": 1700000000,
            "view": "default",
            "zone": "example.com",
        }
    )
    assert r.name == "host.example.com"
    assert r.dhcid == "AAIBY..."
    assert r.creation_time == 1700000000


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_dhcid_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:dhcid/ZG5z:host.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_dhcid.delete("record:dhcid/ZG5z:host.example.com/default")
        assert result == "record:dhcid/ZG5z:host.example.com/default"
