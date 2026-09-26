# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostIpv4addrResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_host_ipv4addr import RecordHostIpv4addr
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


async def test_record_host_ipv4addr_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default",
                        "ipv4addr": "192.168.1.10",
                        "host": "host.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_host_ipv4addr.list(host="host.example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.ipv4addr == "192.168.1.10"
        assert r.host == "host.example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["host"] == "host.example.com"
        assert "ipv4addr" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref) - parses ipv4addr/host/mac fields
# ---------------------------------------------------------------------------


async def test_record_host_ipv4addr_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default",
                "ipv4addr": "192.168.1.10",
                "host": "host.example.com",
                "mac": "aa:bb:cc:dd:ee:ff",
                "configure_for_dhcp": True,
                "comment": "test addr",
            }
        )

    async with _client(handler) as c:
        ref = "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default"
        r = await c.dns.record_host_ipv4addr.get(ref)
        assert r.ipv4addr == "192.168.1.10"
        assert r.host == "host.example.com"
        assert r.mac == "aa:bb:cc:dd:ee:ff"
        assert r.configure_for_dhcp is True


# ---------------------------------------------------------------------------
# 3. find_one(ipv4addr="192.168.1.10") - returns first match
# ---------------------------------------------------------------------------


async def test_record_host_ipv4addr_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default",
                        "ipv4addr": "192.168.1.10",
                        "host": "host.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_host_ipv4addr.find_one(ipv4addr="192.168.1.10")
        assert r is not None
        assert r.ipv4addr == "192.168.1.10"


# ---------------------------------------------------------------------------
# 4. create - POST body correct
# ---------------------------------------------------------------------------


async def test_record_host_ipv4addr_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:host_ipv4addr/NEW:192.168.1.20/host2.example.com/default",
                "ipv4addr": "192.168.1.20",
                "host": "host2.example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_host_ipv4addr.create(
            {"ipv4addr": "192.168.1.20", "mac": "00:11:22:33:44:55", "configure_for_dhcp": True}
        )
        assert r.ipv4addr == "192.168.1.20"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"ipv4addr":"192.168.1.20"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - readonly fields excluded from PUT body
# ---------------------------------------------------------------------------


async def test_record_host_ipv4addr_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default",
                "ipv4addr": "192.168.1.10",
                "host": "host.example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default"
        obj = RecordHostIpv4addr(
            ipv4addr="192.168.1.10",
            mac="aa:bb:cc:dd:ee:ff",
            # readonly fields:
            host="host.example.com",
            last_queried=1700000000,
            network="192.168.1.0/24",
            network_view="default",
            uuid="some-uuid",
            discover_now_status="COMPLETE",
            is_invalid_mac=False,
        )
        await c.dns.record_host_ipv4addr.update(ref, obj)
        body = captured[0].content.decode()

        # Readonly fields must NOT appear
        assert '"host"' not in body, "host is readonly"
        assert '"last_queried"' not in body, "last_queried is readonly"
        assert '"network"' not in body, "network is readonly"
        assert '"network_view"' not in body, "network_view is readonly"
        assert '"uuid"' not in body, "uuid is readonly"
        assert '"discover_now_status"' not in body, "discover_now_status is readonly"
        assert '"is_invalid_mac"' not in body, "is_invalid_mac is readonly"

        # Writable fields must appear
        assert '"ipv4addr":"192.168.1.10"' in body
        assert '"mac":"aa:bb:cc:dd:ee:ff"' in body


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_host_ipv4addr_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_host_ipv4addr.delete(
            "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default"
        )
        assert result == "record:host_ipv4addr/ZG5z:192.168.1.10/host.example.com/default"
