# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordAResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecord_a import SharedrecordA
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(shared_record_group="srg-1") - filter translated to query param
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:a/ZG5z:host.example.com",
                        "name": "host.example.com",
                        "ipv4addr": "192.168.1.10",
                        "shared_record_group": "srg-1",
                        "comment": "shared A",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_a.list(shared_record_group="srg-1").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.ipv4addr == "192.168.1.10"
        assert r.shared_record_group == "srg-1"

        params = captured[0].url.params
        assert params["shared_record_group"] == "srg-1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref) - parses name/ipv4addr/shared_record_group
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecord:a/ZG5z:host.example.com",
                "name": "host.example.com",
                "ipv4addr": "10.0.0.5",
                "shared_record_group": "srg-1",
                "comment": "test record",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:a/ZG5z:host.example.com"
        r = await c.dns.sharedrecord_a.get(ref)
        assert r.name == "host.example.com"
        assert r.ipv4addr == "10.0.0.5"
        assert r.shared_record_group == "srg-1"
        assert r.comment == "test record"


# ---------------------------------------------------------------------------
# 3. find_one(name="host.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:a/ZG5z:host.example.com",
                        "name": "host.example.com",
                        "ipv4addr": "10.0.0.5",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_a.find_one(name="host.example.com")
        assert r is not None
        assert r.name == "host.example.com"
        assert r.ipv4addr == "10.0.0.5"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:a/NEW:host.example.com",
                "name": "host.example.com",
                "ipv4addr": "10.0.0.5",
                "shared_record_group": "srg-1",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_a.create(
            {"name": "host.example.com", "ipv4addr": "10.0.0.5", "shared_record_group": "srg-1"}
        )
        assert r.name == "host.example.com"
        assert r.ipv4addr == "10.0.0.5"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"host.example.com"' in body
        assert '"ipv4addr":"10.0.0.5"' in body
        assert '"shared_record_group":"srg-1"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - PUT body excludes READONLY_FIELDS members
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:a/ZG5z:host.example.com",
                "name": "host.example.com",
                "ipv4addr": "10.0.0.5",
                "shared_record_group": "srg-1",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:a/ZG5z:host.example.com"
        r = SharedrecordA(
            name="host.example.com",
            comment="updated",
            ipv4addr="10.0.0.5",
            dns_name="host.example.com.",  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecord_a.update(ref, r)
        body = captured[0].content.decode()

        # Readonly fields must NOT appear
        assert '"dns_name"' not in body, "dns_name is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"

        # Writable fields must appear
        assert '"name":"host.example.com"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecord:a/ZG5z:host.example.com")

    async with _client(handler) as c:
        result = await c.dns.sharedrecord_a.delete("sharedrecord:a/ZG5z:host.example.com")
        assert result == "sharedrecord:a/ZG5z:host.example.com"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:a/ZG5z:host.example.com",
                        "name": "host.example.com",
                        "ipv4addr": "10.0.0.5",
                        "shared_record_group": "srg-1",
                        "comment": "",
                        "extattrs": {"Site": {"value": "NYC"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_a.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.extattrs is not None
        assert "Site" in r.extattrs
        assert r.extattrs["Site"].value == "NYC"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper - PUT body contains extattrs dict
# ---------------------------------------------------------------------------


async def test_sharedrecord_a_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:a/ZG5z:host.example.com",
                "name": "host.example.com",
                "ipv4addr": "10.0.0.5",
                "shared_record_group": "srg-1",
                "comment": "",
                "extattrs": {"Site": {"value": "NYC"}, "Owner": {"value": "net-eng"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:a/ZG5z:host.example.com"
        await c.dns.sharedrecord_a.set_extattrs(ref, Site="NYC", Owner="net-eng")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert "extattrs" in body_data
        assert body_data["extattrs"]["Site"]["value"] == "NYC"
        assert body_data["extattrs"]["Owner"]["value"] == "net-eng"
