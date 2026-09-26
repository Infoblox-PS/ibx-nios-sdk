# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNsResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_ns import RecordNs
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


async def test_record_ns_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:ns/ZG5z:example.com/default",
                        "name": "example.com",
                        "nameserver": "ns1.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "addresses": [{"address": "192.168.1.1", "auto_create_ptr": False}],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_ns.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.nameserver == "ns1.example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"
        assert "nameserver" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_ns_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:ns/ZG5z:example.com/default",
                "name": "example.com",
                "nameserver": "ns1.example.com",
                "view": "default",
                "zone": "example.com",
                "addresses": [{"address": "192.168.1.1", "auto_create_ptr": False}],
            }
        )

    async with _client(handler) as c:
        ref = "record:ns/ZG5z:example.com/default"
        r = await c.dns.record_ns.get(ref)
        assert r.nameserver == "ns1.example.com"
        assert r.addresses is not None
        assert len(r.addresses) == 1
        assert r.addresses[0].address == "192.168.1.1"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_ns_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:ns/ZG5z:example.com/default",
                        "name": "example.com",
                        "nameserver": "ns1.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "addresses": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_ns.find_one(name="example.com")
        assert r is not None
        assert r.nameserver == "ns1.example.com"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_record_ns_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:ns/NEW:example.com/default",
                "name": "example.com",
                "nameserver": "ns1.example.com",
                "view": "default",
                "zone": "example.com",
                "addresses": [],
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_ns.create(
            {
                "name": "example.com",
                "nameserver": "ns1.example.com",
                "view": "default",
            }
        )
        assert r.nameserver == "ns1.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"nameserver":"ns1.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_record_ns_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:ns/ZG5z:example.com/default",
                "name": "example.com",
                "nameserver": "ns2.example.com",
                "view": "default",
                "zone": "example.com",
                "addresses": [],
            }
        )

    async with _client(handler) as c:
        ref = "record:ns/ZG5z:example.com/default"
        r = RecordNs(
            name="example.com",
            nameserver="ns2.example.com",
            creator="STATIC",  # RO
            dns_name="example.com.",  # RO
            last_queried=1700000001,  # RO
            policy="NIOS",  # RO
            uuid="uuid-123",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_ns.update(ref, r)
        body = captured[0].content.decode()

        assert '"creator"' not in body
        assert '"dns_name"' not in body
        assert '"last_queried"' not in body
        assert '"policy"' not in body
        assert '"zone"' not in body

        assert '"nameserver":"ns2.example.com"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_record_ns_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:ns/ZG5z:example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_ns.delete("record:ns/ZG5z:example.com/default")
        assert result == "record:ns/ZG5z:example.com/default"
