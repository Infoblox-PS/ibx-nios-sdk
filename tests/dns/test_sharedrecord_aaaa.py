# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordAaaaResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecord_aaaa import SharedrecordAaaa
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(shared_record_group="srg-1")
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:aaaa/ZG5z:host.example.com",
                        "name": "host.example.com",
                        "ipv6addr": "2001:db8::1",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_aaaa.list(shared_record_group="srg-1").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"
        assert r.shared_record_group == "srg-1"

        params = captured[0].url.params
        assert params["shared_record_group"] == "srg-1"


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecord:aaaa/ZG5z:host.example.com",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "shared_record_group": "srg-1",
                "comment": "ipv6 record",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:aaaa/ZG5z:host.example.com"
        r = await c.dns.sharedrecord_aaaa.get(ref)
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"
        assert r.comment == "ipv6 record"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:aaaa/ZG5z:host.example.com",
                        "name": "host.example.com",
                        "ipv6addr": "2001:db8::1",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_aaaa.find_one(name="host.example.com")
        assert r is not None
        assert r.ipv6addr == "2001:db8::1"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:aaaa/NEW:host.example.com",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "shared_record_group": "srg-1",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_aaaa.create(
            {"name": "host.example.com", "ipv6addr": "2001:db8::1", "shared_record_group": "srg-1"}
        )
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"ipv6addr":"2001:db8::1"' in body
        assert '"shared_record_group":"srg-1"' in body


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:aaaa/ZG5z:host.example.com",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "shared_record_group": "srg-1",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:aaaa/ZG5z:host.example.com"
        r = SharedrecordAaaa(
            name="host.example.com",
            comment="updated",
            ipv6addr="2001:db8::1",
            dns_name="host.example.com.",  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecord_aaaa.update(ref, r)
        body = captured[0].content.decode()

        assert '"dns_name"' not in body
        assert '"uuid"' not in body
        assert '"name":"host.example.com"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecord:aaaa/ZG5z:host.example.com")

    async with _client(handler) as c:
        result = await c.dns.sharedrecord_aaaa.delete("sharedrecord:aaaa/ZG5z:host.example.com")
        assert result == "sharedrecord:aaaa/ZG5z:host.example.com"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:aaaa/ZG5z:host.example.com",
                        "name": "host.example.com",
                        "ipv6addr": "2001:db8::1",
                        "shared_record_group": "srg-1",
                        "comment": "",
                        "extattrs": {"DC": {"value": "east"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_aaaa.list().all()
        r = records[0]
        assert r.extattrs is not None
        assert r.extattrs["DC"].value == "east"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper
# ---------------------------------------------------------------------------


async def test_sharedrecord_aaaa_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:aaaa/ZG5z:host.example.com",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "shared_record_group": "srg-1",
                "extattrs": {"DC": {"value": "east"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:aaaa/ZG5z:host.example.com"
        await c.dns.sharedrecord_aaaa.set_extattrs(ref, DC="east")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert body_data["extattrs"]["DC"]["value"] == "east"
