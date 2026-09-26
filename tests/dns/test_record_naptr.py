# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNaptrResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_naptr import RecordNaptr
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


async def test_record_naptr_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:naptr/ZG5z:sip.example.com/default",
                        "name": "sip.example.com",
                        "order": 100,
                        "preference": 10,
                        "services": "SIP+D2U",
                        "regexp": "",
                        "replacement": ".",
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_naptr.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "sip.example.com"
        assert r.order == 100
        assert r.preference == 10
        assert r.services == "SIP+D2U"

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="sip")
# ---------------------------------------------------------------------------


async def test_record_naptr_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:naptr/ZG5z:sip.example.com/default",
                        "name": "sip.example.com",
                        "order": 100,
                        "preference": 10,
                        "services": "SIP+D2U",
                        "regexp": "",
                        "replacement": ".",
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_naptr.list(name__like="sip").all()
        assert len(records) == 1
        assert records[0].name == "sip.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_naptr_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:naptr/ZG5z:sip.example.com/default",
                "name": "sip.example.com",
                "order": 100,
                "preference": 10,
                "services": "SIP+D2U",
                "regexp": "",
                "replacement": ".",
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_naptr.get("record:naptr/ZG5z:sip.example.com/default")
        assert r.name == "sip.example.com"
        assert r.order == 100
        assert r.replacement == "."


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_naptr_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:naptr/ZG5z:sip.example.com/default",
                        "name": "sip.example.com",
                        "order": 100,
                        "preference": 10,
                        "services": "SIP+D2U",
                        "regexp": "",
                        "replacement": ".",
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_naptr.find_one(name="sip.example.com")
        assert r is not None
        assert r.name == "sip.example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_naptr_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:naptr/NEW:sip.example.com/default",
                "name": "sip.example.com",
                "order": 100,
                "preference": 10,
                "services": "SIP+D2U",
                "regexp": "",
                "replacement": ".",
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_naptr.create(
            {
                "name": "sip.example.com",
                "order": 100,
                "preference": 10,
                "services": "SIP+D2U",
                "replacement": ".",
            }
        )
        assert r.name == "sip.example.com"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_naptr_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:naptr/ZG5z:sip.example.com/default",
                "name": "sip.example.com",
                "order": 200,
                "preference": 20,
                "services": "SIP+D2T",
                "regexp": "",
                "replacement": ".",
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        ref = "record:naptr/ZG5z:sip.example.com/default"
        r_obj = RecordNaptr(
            name="sip.example.com",
            order=200,
            creation_time=1700000000,  # RO
            dns_name="sip.example.com.",  # RO
            dns_replacement=".",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_naptr.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_name"' not in body
        assert '"dns_replacement"' not in body
        assert '"reclaimable"' not in body
        assert '"zone"' not in body
        assert '"name":"sip.example.com"' in body
