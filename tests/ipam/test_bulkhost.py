# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""BulkhostResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.bulkhost import Bulkhost
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns bulkhost objects
# ---------------------------------------------------------------------------


async def test_bulkhost_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "bulkhost/ZG5z:bh1",
                        "prefix": "host-",
                        "start_addr": "10.0.0.1",
                        "end_addr": "10.0.0.10",
                        "comment": "Bulk host range",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        hosts = await c.ipam.bulkhost.list().all()
        assert len(hosts) == 1
        h = hosts[0]
        assert h.prefix == "host-"
        assert h.start_addr == "10.0.0.1"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "prefix" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_bulkhost_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "bulkhost/ZG5z:bh1",
                        "prefix": "host-",
                        "start_addr": "10.0.0.1",
                        "end_addr": "10.0.0.10",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        hosts = await c.ipam.bulkhost.list(view="default").all()
        assert len(hosts) == 1
        params = captured[0].url.params
        assert params.get("view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_bulkhost_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "bulkhost/ZG5z:bh1",
                "prefix": "host-",
                "start_addr": "10.0.0.1",
                "end_addr": "10.0.0.10",
                "comment": "Bulk host range",
            }
        )

    async with _client(handler) as c:
        ref = "bulkhost/ZG5z:bh1"
        h = await c.ipam.bulkhost.get(ref)
        assert h.prefix == "host-"
        assert h.end_addr == "10.0.0.10"
        assert h.comment == "Bulk host range"


# ---------------------------------------------------------------------------
# 4. find_one(prefix="host-") - returns first match
# ---------------------------------------------------------------------------


async def test_bulkhost_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "bulkhost/ZG5z:bh1",
                        "prefix": "host-",
                        "start_addr": "10.0.0.1",
                        "end_addr": "10.0.0.10",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        h = await c.ipam.bulkhost.find_one(prefix="host-")
        assert h is not None
        assert h.prefix == "host-"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_bulkhost_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "bulkhost/ZG5z:bh2",
                "prefix": "dev-",
                "start_addr": "192.168.1.1",
                "end_addr": "192.168.1.20",
                "comment": "Dev bulk hosts",
            }
        )

    async with _client(handler) as c:
        h = await c.ipam.bulkhost.create(
            {
                "prefix": "dev-",
                "start_addr": "192.168.1.1",
                "end_addr": "192.168.1.20",
                "comment": "Dev bulk hosts",
            }
        )
        assert h.prefix == "dev-"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"prefix":"dev-"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (dns_prefix, last_queried, network_view, etc.)
# ---------------------------------------------------------------------------


async def test_bulkhost_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "bulkhost/ZG5z:bh1",
                "prefix": "host-",
                "start_addr": "10.0.0.1",
                "end_addr": "10.0.0.10",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "bulkhost/ZG5z:bh1"
        bh = Bulkhost(
            prefix="host-",
            comment="updated",
            dns_prefix="host-dns-",  # RO
            network_view="default",  # RO
            uuid="some-uuid",  # RO
            template_format="{n}",  # RO
        )
        await c.ipam.bulkhost.update(ref, bh)
        body = json.loads(captured[0].content.decode())

        assert "dns_prefix" not in body, "dns_prefix is readonly - must be stripped"
        assert "network_view" not in body, "network_view is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert "template_format" not in body, "template_format is readonly - must be stripped"
        assert body.get("comment") == "updated"
