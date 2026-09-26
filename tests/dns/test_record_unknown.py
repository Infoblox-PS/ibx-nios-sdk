# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordUnknownResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_unknown import RecordUnknown
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


async def test_record_unknown_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:unknown/ZG5z:custom.example.com/default",
                        "name": "custom.example.com",
                        "record_type": "TYPE1234",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_unknown.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "custom.example.com"
        assert r.record_type == "TYPE1234"

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="custom")
# ---------------------------------------------------------------------------


async def test_record_unknown_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:unknown/ZG5z:custom.example.com/default",
                        "name": "custom.example.com",
                        "record_type": "TYPE1234",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_unknown.list(name__like="custom").all()
        assert len(records) == 1
        assert records[0].name == "custom.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_unknown_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:unknown/ZG5z:custom.example.com/default",
                "name": "custom.example.com",
                "record_type": "TYPE1234",
                "view": "default",
                "zone": "example.com",
                "comment": "unknown record",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_unknown.get("record:unknown/ZG5z:custom.example.com/default")
        assert r.name == "custom.example.com"
        assert r.record_type == "TYPE1234"
        assert r.comment == "unknown record"


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_unknown_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:unknown/ZG5z:custom.example.com/default",
                        "name": "custom.example.com",
                        "record_type": "TYPE1234",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_unknown.find_one(name="custom.example.com")
        assert r is not None
        assert r.name == "custom.example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_unknown_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:unknown/NEW:custom.example.com/default",
                "name": "custom.example.com",
                "record_type": "TYPE1234",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_unknown.create(
            {"name": "custom.example.com", "record_type": "TYPE1234"}
        )
        assert r.name == "custom.example.com"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_unknown_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:unknown/ZG5z:custom.example.com/default",
                "name": "custom.example.com",
                "record_type": "TYPE1234",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:unknown/ZG5z:custom.example.com/default"
        r_obj = RecordUnknown(
            name="custom.example.com",
            comment="updated",
            display_rdata="\\# 4 0a000001",  # RO
            dns_name="custom.example.com.",  # RO
            last_queried=1700000001,  # RO
            policy="NXDOMAIN",  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_unknown.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"display_rdata"' not in body
        assert '"dns_name"' not in body
        assert '"last_queried"' not in body
        assert '"policy"' not in body
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"name":"custom.example.com"' in body
        assert '"comment":"updated"' in body
