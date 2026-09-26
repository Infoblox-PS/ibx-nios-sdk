# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDnameResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_dname import RecordDname
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


async def test_record_dname_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:dname/ZG5z:sub.example.com/default",
                        "name": "sub.example.com",
                        "target": "other.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_dname.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "sub.example.com"
        assert r.target == "other.example.com"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="sub")
# ---------------------------------------------------------------------------


async def test_record_dname_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:dname/ZG5z:sub.example.com/default",
                        "name": "sub.example.com",
                        "target": "other.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_dname.list(name__like="sub").all()
        assert len(records) == 1
        assert records[0].name == "sub.example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_dname_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:dname/ZG5z:sub.example.com/default",
                "name": "sub.example.com",
                "target": "other.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "dname record",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_dname.get("record:dname/ZG5z:sub.example.com/default")
        assert r.name == "sub.example.com"
        assert r.target == "other.example.com"
        assert r.comment == "dname record"


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_dname_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:dname/ZG5z:sub.example.com/default",
                        "name": "sub.example.com",
                        "target": "other.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_dname.find_one(name="sub.example.com")
        assert r is not None
        assert r.name == "sub.example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_dname_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:dname/NEW:sub.example.com/default",
                "name": "sub.example.com",
                "target": "other.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_dname.create(
            {"name": "sub.example.com", "target": "other.example.com", "view": "default"}
        )
        assert r.name == "sub.example.com"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_dname_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:dname/ZG5z:sub.example.com/default",
                "name": "sub.example.com",
                "target": "other.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:dname/ZG5z:sub.example.com/default"
        r_obj = RecordDname(
            name="sub.example.com",
            comment="updated",
            creation_time=1700000000,  # RO
            dns_name="sub.example.com.",  # RO
            dns_target="other.example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            shared_record_group="srg1",  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_dname.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_name"' not in body
        assert '"dns_target"' not in body
        assert '"reclaimable"' not in body
        assert '"zone"' not in body
        assert '"name":"sub.example.com"' in body
        assert '"comment":"updated"' in body
