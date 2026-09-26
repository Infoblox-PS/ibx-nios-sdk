# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostResource - CRUD, find_one, list, extattrs, readonly-strip, nested addrs."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_host import RecordHost
from ibx_nios_sdk.dns.models.record_host_ipv4addr import RecordHostIpv4addr
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(zone="example.com") - filter present in params
# ---------------------------------------------------------------------------


async def test_record_host_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:host/ZG5z:host.example.com/default",
                        "name": "host.example.com",
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
        records = await c.dns.record_host.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["zone"] == "example.com"
        assert "name" in params["_return_fields+"]
        assert "view" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref) - parses name/view/zone/comment and nested ipv4addrs
# ---------------------------------------------------------------------------


async def test_record_host_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:host/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "web server",
                "disable": False,
                "ipv4addrs": [
                    {
                        "_ref": "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default",
                        "ipv4addr": "192.168.1.10",
                        "host": "host.example.com",
                    }
                ],
                "ipv6addrs": [],
            }
        )

    async with _client(handler) as c:
        ref = "record:host/ZG5z:host.example.com/default"
        r = await c.dns.record_host.get(ref)
        assert r.name == "host.example.com"
        assert r.view == "default"
        assert r.comment == "web server"
        # nested ipv4addrs should be typed RecordHostIpv4addr objects
        assert r.ipv4addrs is not None
        assert len(r.ipv4addrs) == 1
        addr = r.ipv4addrs[0]
        assert isinstance(addr, RecordHostIpv4addr)
        assert addr.ipv4addr == "192.168.1.10"
        assert addr.host == "host.example.com"


# ---------------------------------------------------------------------------
# 3. find_one(name="host.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_record_host_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:host/ZG5z:host.example.com/default",
                        "name": "host.example.com",
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
        r = await c.dns.record_host.find_one(name="host.example.com")
        assert r is not None
        assert r.name == "host.example.com"


# ---------------------------------------------------------------------------
# 4. create - POST body correct, _return_as_object=1
# ---------------------------------------------------------------------------


async def test_record_host_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:host/NEW:host.example.com/default",
                "name": "host.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_host.create(
            {
                "name": "host.example.com",
                "view": "default",
                "ipv4addrs": [{"ipv4addr": "192.168.1.10"}],
            }
        )
        assert r.name == "host.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"host.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - readonly fields excluded from PUT body
# ---------------------------------------------------------------------------


async def test_record_host_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:host/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:host/ZG5z:host.example.com/default"
        r = RecordHost(
            name="host.example.com",
            comment="updated",
            view="default",
            # readonly fields:
            creation_time=1700000000,
            dns_name="host.example.com.",
            last_queried=1700000001,
            uuid="some-uuid",
            zone="example.com",
        )
        await c.dns.record_host.update(ref, r)
        body = captured[0].content.decode()

        # Readonly fields must NOT appear
        assert '"creation_time"' not in body, "creation_time is readonly"
        assert '"dns_name"' not in body, "dns_name is readonly"
        assert '"last_queried"' not in body, "last_queried is readonly"
        assert '"uuid"' not in body, "uuid is readonly"
        assert '"zone"' not in body, "zone is readonly"

        # Writable fields must appear
        assert '"name":"host.example.com"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_host_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:host/ZG5z:host.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_host.delete("record:host/ZG5z:host.example.com/default")
        assert result == "record:host/ZG5z:host.example.com/default"
