# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networkResource - CRUD, find_one, list, extattrs, readonly-strip, next_available_ip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.ipv6network import Ipv6network
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns ipv6network objects
# ---------------------------------------------------------------------------


async def test_ipv6network_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6network/ZG5z:2001:db8::/64/default",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        nets = await c.ipam.ipv6network.list().all()
        assert len(nets) == 1
        n = nets[0]
        assert n.network == "2001:db8::/64"
        assert n.network_view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "network" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_ipv6network_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6network/ZG5z:2001:db8::/64/default",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        nets = await c.ipam.ipv6network.list(network_view="default").all()
        assert len(nets) == 1

        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_ipv6network_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ipv6network/ZG5z:2001:db8::/64/default",
                "network": "2001:db8::/64",
                "network_view": "default",
                "comment": "Production IPv6 network",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "ipv6network/ZG5z:2001:db8::/64/default"
        n = await c.ipam.ipv6network.get(ref)
        assert n.network == "2001:db8::/64"
        assert n.network_view == "default"
        assert n.comment == "Production IPv6 network"


# ---------------------------------------------------------------------------
# 4. find_one(network="2001:db8::/64") - returns first match
# ---------------------------------------------------------------------------


async def test_ipv6network_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6network/ZG5z:2001:db8::/64/default",
                        "network": "2001:db8::/64",
                        "network_view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        n = await c.ipam.ipv6network.find_one(network="2001:db8::/64")
        assert n is not None
        assert n.network == "2001:db8::/64"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_ipv6network_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6network/ZG5z:2001:db8:1::/48/default",
                "network": "2001:db8:1::/48",
                "network_view": "default",
                "comment": "New IPv6 network",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        n = await c.ipam.ipv6network.create(
            {
                "network": "2001:db8:1::/48",
                "network_view": "default",
                "comment": "New IPv6 network",
            }
        )
        assert n.network == "2001:db8:1::/48"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert "2001:db8:1::/48" in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {...}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_ipv6network_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6network/ZG5z:2001:db8::/64/default",
                "network": "2001:db8::/64",
                "network_view": "default",
                "comment": "Updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "ipv6network/ZG5z:2001:db8::/64/default"
        n = await c.ipam.ipv6network.update(ref, {"comment": "Updated"})
        assert n.comment == "Updated"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path


# ---------------------------------------------------------------------------
# Extra: readonly-strip on update
# ---------------------------------------------------------------------------


async def test_ipv6network_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6network/ZG5z:2001:db8::/64/default",
                "network": "2001:db8::/64",
                "network_view": "default",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "ipv6network/ZG5z:2001:db8::/64/default"
        net = Ipv6network(
            network="2001:db8::/64",
            comment="updated",
            unmanaged_count=5,  # RO
            uuid="some-uuid",  # RO
            rir="ARIN",  # RO
        )
        await c.ipam.ipv6network.update(ref, net)
        body = json.loads(captured[0].content.decode())

        assert "unmanaged_count" not in body, "unmanaged_count is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert "rir" not in body, "rir is readonly - must be stripped"
        assert body.get("comment") == "updated"


# ---------------------------------------------------------------------------
# Function call: next_available_ip
# ---------------------------------------------------------------------------


async def test_ipv6network_next_available_ip() -> None:
    """POST to /{ref}?_function=next_available_ip with body {"num": 2}."""
    captured: list[httpx.Request] = []
    expected_ips = ["2001:db8::5", "2001:db8::6"]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": expected_ips})

    async with _client(handler) as c:
        ref = "ipv6network/ZG5z:2001:db8::/64/default"
        result = await c.ipam.ipv6network.next_available_ip(ref, num=2)

        assert result["ips"] == expected_ips

        req = captured[0]
        assert req.method == "POST"
        assert ref in req.url.path
        assert req.url.params.get("_function") == "next_available_ip"

        body = json.loads(req.content.decode())
        assert body["num"] == 2
        assert "exclude" not in body


async def test_ipv6network_next_available_ip_with_exclude() -> None:
    """Passing exclude must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": ["2001:db8::10"]})

    async with _client(handler) as c:
        ref = "ipv6network/ZG5z:2001:db8::/64/default"
        result = await c.ipam.ipv6network.next_available_ip(ref, num=1, exclude=["2001:db8::1"])
        assert result["ips"] == ["2001:db8::10"]
        body = json.loads(captured[0].content.decode())
        assert body["exclude"] == ["2001:db8::1"]
