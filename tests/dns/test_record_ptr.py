# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordPtrResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_ptr import RecordPtr
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(view="default")
# ---------------------------------------------------------------------------


async def test_record_ptr_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default",
                        "ptrdname": "host.example.com",
                        "ipv4addr": "192.168.1.1",
                        "name": "1.1.168.192.in-addr.arpa",
                        "view": "default",
                        "zone": "1.168.192.in-addr.arpa",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_ptr.list(view="default").all()
        assert len(records) == 1
        r = records[0]
        assert r.ptrdname == "host.example.com"
        assert r.ipv4addr == "192.168.1.1"

        params = captured[0].url.params
        assert params["view"] == "default"
        assert "ptrdname" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_ptr_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default",
                "ptrdname": "host.example.com",
                "ipv4addr": "192.168.1.1",
                "name": "1.1.168.192.in-addr.arpa",
                "view": "default",
                "zone": "1.168.192.in-addr.arpa",
                "comment": "ptr record",
            }
        )

    async with _client(handler) as c:
        ref = "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default"
        r = await c.dns.record_ptr.get(ref)
        assert r.ptrdname == "host.example.com"
        assert r.ipv4addr == "192.168.1.1"
        assert r.comment == "ptr record"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_ptr_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default",
                        "ptrdname": "host.example.com",
                        "ipv4addr": "192.168.1.1",
                        "name": "1.1.168.192.in-addr.arpa",
                        "view": "default",
                        "zone": "1.168.192.in-addr.arpa",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_ptr.find_one(ptrdname="host.example.com")
        assert r is not None
        assert r.ptrdname == "host.example.com"
        assert r.ipv4addr == "192.168.1.1"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_record_ptr_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:ptr/NEW:1.1.168.192.in-addr.arpa/default",
                "ptrdname": "host.example.com",
                "ipv4addr": "192.168.1.1",
                "name": "1.1.168.192.in-addr.arpa",
                "view": "default",
                "zone": "1.168.192.in-addr.arpa",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_ptr.create(
            {"ptrdname": "host.example.com", "ipv4addr": "192.168.1.1", "view": "default"}
        )
        assert r.ptrdname == "host.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"ptrdname":"host.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_record_ptr_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default",
                "ptrdname": "host2.example.com",
                "ipv4addr": "192.168.1.1",
                "name": "1.1.168.192.in-addr.arpa",
                "view": "default",
                "zone": "1.168.192.in-addr.arpa",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default"
        r = RecordPtr(
            ptrdname="host2.example.com",
            ipv4addr="192.168.1.1",
            comment="updated",
            creation_time=1700000000,  # RO
            dns_name="1.1.168.192.in-addr.arpa.",  # RO
            dns_ptrdname="host2.example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
            zone="1.168.192.in-addr.arpa",  # RO
        )
        await c.dns.record_ptr.update(ref, r)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_name"' not in body
        assert '"dns_ptrdname"' not in body
        assert '"last_queried"' not in body
        assert '"reclaimable"' not in body
        assert '"shared_record_group"' not in body
        assert '"zone"' not in body

        assert '"ptrdname":"host2.example.com"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_record_ptr_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default")

    async with _client(handler) as c:
        result = await c.dns.record_ptr.delete("record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default")
        assert result == "record:ptr/ZG5z:1.1.168.192.in-addr.arpa/default"
