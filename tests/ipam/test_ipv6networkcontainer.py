# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networkcontainerResource - CRUD, find_one, list, extattrs, readonly-strip, next_available_network."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.ipv6networkcontainer import Ipv6networkcontainer
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns ipv6networkcontainer objects
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6networkcontainer/ZG5z:2001:db8::/32/default",
                        "network": "2001:db8::/32",
                        "network_view": "default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        containers = await c.ipam.ipv6networkcontainer.list().all()
        assert len(containers) == 1
        nc = containers[0]
        assert nc.network == "2001:db8::/32"
        assert nc.network_view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "network" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6networkcontainer/ZG5z:2001:db8::/32/default",
                        "network": "2001:db8::/32",
                        "network_view": "default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        containers = await c.ipam.ipv6networkcontainer.list(network_view="default").all()
        assert len(containers) == 1

        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ipv6networkcontainer/ZG5z:2001:db8::/32/default",
                "network": "2001:db8::/32",
                "network_view": "default",
                "comment": "Main IPv6 supernet",
            }
        )

    async with _client(handler) as c:
        ref = "ipv6networkcontainer/ZG5z:2001:db8::/32/default"
        nc = await c.ipam.ipv6networkcontainer.get(ref)
        assert nc.network == "2001:db8::/32"
        assert nc.comment == "Main IPv6 supernet"


# ---------------------------------------------------------------------------
# 4. find_one(network="2001:db8::/32") - returns first match
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6networkcontainer/ZG5z:2001:db8::/32/default",
                        "network": "2001:db8::/32",
                        "network_view": "default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        nc = await c.ipam.ipv6networkcontainer.find_one(network="2001:db8::/32")
        assert nc is not None
        assert nc.network == "2001:db8::/32"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6networkcontainer/ZG5z:2001:db8:1::/48/default",
                "network": "2001:db8:1::/48",
                "network_view": "default",
                "comment": "New IPv6 container",
            }
        )

    async with _client(handler) as c:
        nc = await c.ipam.ipv6networkcontainer.create(
            {
                "network": "2001:db8:1::/48",
                "network_view": "default",
                "comment": "New IPv6 container",
            }
        )
        assert nc.network == "2001:db8:1::/48"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {...}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6networkcontainer/ZG5z:2001:db8::/32/default",
                "network": "2001:db8::/32",
                "network_view": "default",
                "comment": "Updated",
            }
        )

    async with _client(handler) as c:
        ref = "ipv6networkcontainer/ZG5z:2001:db8::/32/default"
        nc = await c.ipam.ipv6networkcontainer.update(ref, {"comment": "Updated"})
        assert nc.comment == "Updated"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path


# ---------------------------------------------------------------------------
# Extra: readonly-strip on update
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6networkcontainer/ZG5z:2001:db8::/32/default",
                "network": "2001:db8::/32",
                "network_view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "ipv6networkcontainer/ZG5z:2001:db8::/32/default"
        nc = Ipv6networkcontainer(
            network="2001:db8::/32",
            comment="updated",
            utilization=50,  # RO
            uuid="some-uuid",  # RO
            rir="ARIN",  # RO
        )
        await c.ipam.ipv6networkcontainer.update(ref, nc)
        body = json.loads(captured[0].content.decode())

        assert "utilization" not in body, "utilization is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert "rir" not in body, "rir is readonly - must be stripped"
        assert body.get("comment") == "updated"


# ---------------------------------------------------------------------------
# Function call: next_available_network
# ---------------------------------------------------------------------------


async def test_ipv6networkcontainer_next_available_network() -> None:
    """POST to /{ref}?_function=next_available_network with body {"cidr": 64, "num": 2}."""
    captured: list[httpx.Request] = []
    expected_networks = ["2001:db8::/64", "2001:db8:0:1::/64"]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"networks": expected_networks})

    async with _client(handler) as c:
        ref = "ipv6networkcontainer/ZG5z:2001:db8::/32/default"
        result = await c.ipam.ipv6networkcontainer.next_available_network(ref, cidr=64, num=2)

        assert result["networks"] == expected_networks

        req = captured[0]
        assert req.method == "POST"
        assert ref in req.url.path
        assert req.url.params.get("_function") == "next_available_network"

        body = json.loads(req.content.decode())
        assert body["cidr"] == 64
        assert body["num"] == 2
        assert "exclude" not in body


async def test_ipv6networkcontainer_next_available_network_with_exclude() -> None:
    """Passing exclude must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"networks": ["2001:db8:0:2::/64"]})

    async with _client(handler) as c:
        ref = "ipv6networkcontainer/ZG5z:2001:db8::/32/default"
        result = await c.ipam.ipv6networkcontainer.next_available_network(
            ref, cidr=64, num=1, exclude=["2001:db8::/64"]
        )
        assert result["networks"] == ["2001:db8:0:2::/64"]
        body = json.loads(captured[0].content.decode())
        assert body["exclude"] == ["2001:db8::/64"]
