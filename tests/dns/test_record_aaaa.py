# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordAaaaResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_aaaa import RecordAaaa
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(view="default") - filter translated to view=default
# ---------------------------------------------------------------------------


async def test_record_aaaa_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:aaaa/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "ipv6addr": "2001:db8::1",
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
        records = await c.dns.record_aaaa.list(view="default").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"
        assert r.view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "name" in params["_return_fields+"]
        assert "ipv6addr" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref) - parses name/ipv6addr/view/comment
# ---------------------------------------------------------------------------


async def test_record_aaaa_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:aaaa/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "view": "default",
                "zone": "example.com",
                "comment": "ipv6 host",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:aaaa/ZG5z:host.example.com/default"
        r = await c.dns.record_aaaa.get(ref)
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"
        assert r.view == "default"
        assert r.comment == "ipv6 host"


# ---------------------------------------------------------------------------
# 3. find_one(name="host.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_record_aaaa_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:aaaa/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "ipv6addr": "2001:db8::1",
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
        r = await c.dns.record_aaaa.find_one(name="host.example.com")
        assert r is not None
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"


# ---------------------------------------------------------------------------
# 4. create - POST body correct, _return_as_object=1
# ---------------------------------------------------------------------------


async def test_record_aaaa_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:aaaa/NEW:host.example.com/default",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "view": "default",
                "zone": "example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_aaaa.create(
            {"name": "host.example.com", "ipv6addr": "2001:db8::1", "view": "default"}
        )
        assert r.name == "host.example.com"
        assert r.ipv6addr == "2001:db8::1"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"host.example.com"' in body
        assert '"ipv6addr":"2001:db8::1"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - PUT body excludes readonly fields
# ---------------------------------------------------------------------------


async def test_record_aaaa_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:aaaa/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "ipv6addr": "2001:db8::1",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:aaaa/ZG5z:host.example.com/default"
        r = RecordAaaa(
            name="host.example.com",
            comment="updated",
            ipv6addr="2001:db8::1",
            creation_time=1700000000,  # RO
            last_queried=1700000001,  # RO
            dns_name="host.example.com.",  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_aaaa.update(ref, r)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"last_queried"' not in body
        assert '"dns_name"' not in body
        assert '"reclaimable"' not in body
        assert '"shared_record_group"' not in body
        assert '"zone"' not in body

        assert '"name":"host.example.com"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_aaaa_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:aaaa/ZG5z:host.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_aaaa.delete("record:aaaa/ZG5z:host.example.com/default")
        assert result == "record:aaaa/ZG5z:host.example.com/default"
