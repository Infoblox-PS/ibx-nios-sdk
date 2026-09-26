# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordTlsaResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_tlsa import RecordTlsa
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


async def test_record_tlsa_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:tlsa/ZG5z:_443._tcp.example.com/default",
                        "name": "_443._tcp.example.com",
                        "certificate_usage": 3,
                        "selector": 1,
                        "matched_type": 1,
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_tlsa.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "_443._tcp.example.com"
        assert r.certificate_usage == 3
        assert r.selector == 1

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="_443")
# ---------------------------------------------------------------------------


async def test_record_tlsa_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:tlsa/ZG5z:_443._tcp.example.com/default",
                        "name": "_443._tcp.example.com",
                        "certificate_usage": 3,
                        "selector": 1,
                        "matched_type": 1,
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_tlsa.list(name__like="_443").all()
        assert len(records) == 1
        assert records[0].name == "_443._tcp.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_tlsa_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:tlsa/ZG5z:_443._tcp.example.com/default",
                "name": "_443._tcp.example.com",
                "certificate_usage": 3,
                "selector": 1,
                "matched_type": 1,
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_tlsa.get("record:tlsa/ZG5z:_443._tcp.example.com/default")
        assert r.name == "_443._tcp.example.com"
        assert r.certificate_usage == 3
        assert r.selector == 1


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_tlsa_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:tlsa/ZG5z:_443._tcp.example.com/default",
                        "name": "_443._tcp.example.com",
                        "certificate_usage": 3,
                        "selector": 1,
                        "matched_type": 1,
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_tlsa.find_one(name="_443._tcp.example.com")
        assert r is not None
        assert r.name == "_443._tcp.example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_tlsa_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:tlsa/NEW:_443._tcp.example.com/default",
                "name": "_443._tcp.example.com",
                "certificate_usage": 3,
                "selector": 1,
                "matched_type": 1,
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_tlsa.create(
            {
                "name": "_443._tcp.example.com",
                "certificate_usage": 3,
                "selector": 1,
                "matched_type": 1,
            }
        )
        assert r.name == "_443._tcp.example.com"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_tlsa_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:tlsa/ZG5z:_443._tcp.example.com/default",
                "name": "_443._tcp.example.com",
                "certificate_usage": 3,
                "selector": 1,
                "matched_type": 1,
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        ref = "record:tlsa/ZG5z:_443._tcp.example.com/default"
        r_obj = RecordTlsa(
            name="_443._tcp.example.com",
            certificate_usage=3,
            dns_name="_443._tcp.example.com.",  # RO
            last_queried=1700000001,  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_tlsa.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"dns_name"' not in body
        assert '"last_queried"' not in body
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"name":"_443._tcp.example.com"' in body
