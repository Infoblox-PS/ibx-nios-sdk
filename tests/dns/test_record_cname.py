# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordCnameResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_cname import RecordCname
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


async def test_record_cname_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:cname/ZG5z:alias.example.com/default",
                        "name": "alias.example.com",
                        "canonical": "host.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_cname.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "alias.example.com"
        assert r.canonical == "host.example.com"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"
        assert "name" in params["_return_fields+"]
        assert "canonical" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_cname_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:cname/ZG5z:alias.example.com/default",
                "name": "alias.example.com",
                "canonical": "host.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "cname record",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:cname/ZG5z:alias.example.com/default"
        r = await c.dns.record_cname.get(ref)
        assert r.name == "alias.example.com"
        assert r.canonical == "host.example.com"
        assert r.comment == "cname record"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_cname_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:cname/ZG5z:alias.example.com/default",
                        "name": "alias.example.com",
                        "canonical": "host.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_cname.find_one(name="alias.example.com")
        assert r is not None
        assert r.canonical == "host.example.com"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_record_cname_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:cname/NEW:alias.example.com/default",
                "name": "alias.example.com",
                "canonical": "host.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_cname.create(
            {"name": "alias.example.com", "canonical": "host.example.com", "view": "default"}
        )
        assert r.canonical == "host.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"canonical":"host.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_record_cname_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:cname/ZG5z:alias.example.com/default",
                "name": "alias.example.com",
                "canonical": "host2.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:cname/ZG5z:alias.example.com/default"
        r = RecordCname(
            name="alias.example.com",
            canonical="host2.example.com",
            comment="updated",
            creation_time=1700000000,  # RO
            dns_canonical="host2.example.com.",  # RO
            dns_name="alias.example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
            uuid="uuid-123",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_cname.update(ref, r)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_canonical"' not in body
        assert '"dns_name"' not in body
        assert '"last_queried"' not in body
        assert '"reclaimable"' not in body
        assert '"shared_record_group"' not in body
        assert '"zone"' not in body

        assert '"canonical":"host2.example.com"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_record_cname_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:cname/ZG5z:alias.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_cname.delete("record:cname/ZG5z:alias.example.com/default")
        assert result == "record:cname/ZG5z:alias.example.com/default"
