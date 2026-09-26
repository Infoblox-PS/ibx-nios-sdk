# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostIpv6addrResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_host_ipv6addr import RecordHostIpv6addr
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(host="host.example.com") - filter present in request params
# ---------------------------------------------------------------------------


async def test_record_host_ipv6addr_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default",
                        "ipv6addr": "2001:db8::1",
                        "host": "host.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_host_ipv6addr.list(host="host.example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.ipv6addr == "2001:db8::1"
        assert r.host == "host.example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["host"] == "host.example.com"
        assert "ipv6addr" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref) - parses ipv6addr/host fields
# ---------------------------------------------------------------------------


async def test_record_host_ipv6addr_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default",
                "ipv6addr": "2001:db8::1",
                "host": "host.example.com",
                "duid": "00:01:02:03",
                "configure_for_dhcp": True,
                "comment": "test v6 addr",
            }
        )

    async with _client(handler) as c:
        ref = "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default"
        r = await c.dns.record_host_ipv6addr.get(ref)
        assert r.ipv6addr == "2001:db8::1"
        assert r.host == "host.example.com"
        assert r.duid == "00:01:02:03"
        assert r.configure_for_dhcp is True


# ---------------------------------------------------------------------------
# 3. find_one(ipv6addr="2001:db8::1") - returns first match
# ---------------------------------------------------------------------------


async def test_record_host_ipv6addr_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default",
                        "ipv6addr": "2001:db8::1",
                        "host": "host.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_host_ipv6addr.find_one(ipv6addr="2001:db8::1")
        assert r is not None
        assert r.ipv6addr == "2001:db8::1"


# ---------------------------------------------------------------------------
# 4. create - POST body correct
# ---------------------------------------------------------------------------


async def test_record_host_ipv6addr_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:host_ipv6addr/NEW:2001:db8::2/host2.example.com/default",
                "ipv6addr": "2001:db8::2",
                "host": "host2.example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_host_ipv6addr.create(
            {"ipv6addr": "2001:db8::2", "configure_for_dhcp": True}
        )
        assert r.ipv6addr == "2001:db8::2"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"ipv6addr":"2001:db8::2"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - readonly fields excluded from PUT body
# ---------------------------------------------------------------------------


async def test_record_host_ipv6addr_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default",
                "ipv6addr": "2001:db8::1",
                "host": "host.example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default"
        obj = RecordHostIpv6addr(
            ipv6addr="2001:db8::1",
            duid="00:01:02:03",
            # readonly fields:
            host="host.example.com",
            last_queried=1700000000,
            network="2001:db8::/32",
            network_view="default",
            uuid="some-uuid",
            discover_now_status="COMPLETE",
        )
        await c.dns.record_host_ipv6addr.update(ref, obj)
        body = captured[0].content.decode()

        # Readonly fields must NOT appear
        assert '"host"' not in body, "host is readonly"
        assert '"last_queried"' not in body, "last_queried is readonly"
        assert '"network"' not in body, "network is readonly"
        assert '"network_view"' not in body, "network_view is readonly"
        assert '"uuid"' not in body, "uuid is readonly"
        assert '"discover_now_status"' not in body, "discover_now_status is readonly"

        # Writable fields must appear
        assert '"ipv6addr":"2001:db8::1"' in body
        assert '"duid":"00:01:02:03"' in body


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_host_ipv6addr_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_host_ipv6addr.delete(
            "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default"
        )
        assert result == "record:host_ipv6addr/ZG5z:2001:db8::1/host.example.com/default"
