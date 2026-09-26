# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordSvcbResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_svcb import RecordSvcb
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


async def test_record_svcb_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:svcb/ZG5z:svcb.example.com/default",
                        "name": "svcb.example.com",
                        "priority": 1,
                        "target_name": "backend.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_svcb.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "svcb.example.com"
        assert r.priority == 1
        assert r.target_name == "backend.example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="svcb")
# ---------------------------------------------------------------------------


async def test_record_svcb_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:svcb/ZG5z:svcb.example.com/default",
                        "name": "svcb.example.com",
                        "priority": 1,
                        "target_name": "backend.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_svcb.list(name__like="svcb").all()
        assert len(records) == 1
        assert records[0].name == "svcb.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_svcb_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:svcb/ZG5z:svcb.example.com/default",
                "name": "svcb.example.com",
                "priority": 1,
                "target_name": "backend.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "svcb record",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_svcb.get("record:svcb/ZG5z:svcb.example.com/default")
        assert r.name == "svcb.example.com"
        assert r.priority == 1
        assert r.comment == "svcb record"


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_svcb_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:svcb/ZG5z:svcb.example.com/default",
                        "name": "svcb.example.com",
                        "priority": 1,
                        "target_name": "backend.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_svcb.find_one(name="svcb.example.com")
        assert r is not None
        assert r.name == "svcb.example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_svcb_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:svcb/NEW:svcb.example.com/default",
                "name": "svcb.example.com",
                "priority": 1,
                "target_name": "backend.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_svcb.create(
            {
                "name": "svcb.example.com",
                "priority": 1,
                "target_name": "backend.example.com",
            }
        )
        assert r.name == "svcb.example.com"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_svcb_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:svcb/ZG5z:svcb.example.com/default",
                "name": "svcb.example.com",
                "priority": 2,
                "target_name": "backend.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:svcb/ZG5z:svcb.example.com/default"
        r_obj = RecordSvcb(
            name="svcb.example.com",
            comment="updated",
            creation_time=1700000000,  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_svcb.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"last_queried"' not in body
        assert '"reclaimable"' not in body
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"name":"svcb.example.com"' in body
        assert '"comment":"updated"' in body
