# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkResource - CRUD, find_one, list, extattrs, readonly-strip, next_available_ip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.network import Network
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns network objects
# ---------------------------------------------------------------------------


async def test_network_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "network/ZG5z:10.0.0.0/24/default",
                        "network": "10.0.0.0/24",
                        "network_view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        nets = await c.ipam.network.list().all()
        assert len(nets) == 1
        n = nets[0]
        assert n.network == "10.0.0.0/24"
        assert n.network_view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "network" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_network_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "network/ZG5z:10.0.0.0/24/default",
                        "network": "10.0.0.0/24",
                        "network_view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        nets = await c.ipam.network.list(network_view="default").all()
        assert len(nets) == 1

        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_network_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "network/ZG5z:10.0.0.0/24/default",
                "network": "10.0.0.0/24",
                "network_view": "default",
                "comment": "Production network",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "network/ZG5z:10.0.0.0/24/default"
        n = await c.ipam.network.get(ref)
        assert n.network == "10.0.0.0/24"
        assert n.network_view == "default"
        assert n.comment == "Production network"


# ---------------------------------------------------------------------------
# 4. find_one(network="10.0.0.0/24") - returns first match
# ---------------------------------------------------------------------------


async def test_network_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "network/ZG5z:10.0.0.0/24/default",
                        "network": "10.0.0.0/24",
                        "network_view": "default",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        n = await c.ipam.network.find_one(network="10.0.0.0/24")
        assert n is not None
        assert n.network == "10.0.0.0/24"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_network_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "network/ZG5z:192.168.1.0/24/default",
                "network": "192.168.1.0/24",
                "network_view": "default",
                "comment": "New network",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        n = await c.ipam.network.create(
            {"network": "192.168.1.0/24", "network_view": "default", "comment": "New network"}
        )
        assert n.network == "192.168.1.0/24"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"network":"192.168.1.0/24"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {...}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_network_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "network/ZG5z:10.0.0.0/24/default",
                "network": "10.0.0.0/24",
                "network_view": "default",
                "comment": "Updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "network/ZG5z:10.0.0.0/24/default"
        n = await c.ipam.network.update(ref, {"comment": "Updated"})
        assert n.comment == "Updated"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path


# ---------------------------------------------------------------------------
# Extra: readonly-strip on update
# ---------------------------------------------------------------------------


async def test_network_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "network/ZG5z:10.0.0.0/24/default",
                "network": "10.0.0.0/24",
                "network_view": "default",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "network/ZG5z:10.0.0.0/24/default"
        net = Network(
            network="10.0.0.0/24",
            comment="updated",
            utilization=75,  # RO
            uuid="some-uuid",  # RO
            static_hosts=10,  # RO
        )
        await c.ipam.network.update(ref, net)
        body = json.loads(captured[0].content.decode())

        assert "utilization" not in body, "utilization is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert "static_hosts" not in body, "static_hosts is readonly - must be stripped"
        assert body.get("comment") == "updated"


# ---------------------------------------------------------------------------
# Function call: next_available_ip
# ---------------------------------------------------------------------------


async def test_network_next_available_ip() -> None:
    """POST to /{ref}?_function=next_available_ip with body {"num": 3}."""
    captured: list[httpx.Request] = []
    expected_ips = ["10.0.0.5", "10.0.0.6", "10.0.0.7"]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": expected_ips})

    async with _client(handler) as c:
        ref = "network/ZG5z:10.0.0.0/24/default"
        result = await c.ipam.network.next_available_ip(ref, num=3)

        assert result["ips"] == expected_ips

        req = captured[0]
        assert req.method == "POST"
        assert ref in req.url.path
        assert req.url.params.get("_function") == "next_available_ip"

        body = json.loads(req.content.decode())
        assert body["num"] == 3
        assert "exclude" not in body


async def test_network_next_available_ip_with_exclude() -> None:
    """Passing exclude must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": ["10.0.0.10"]})

    async with _client(handler) as c:
        ref = "network/ZG5z:10.0.0.0/24/default"
        result = await c.ipam.network.next_available_ip(ref, num=1, exclude=["10.0.0.1"])
        assert result["ips"] == ["10.0.0.10"]
        body = json.loads(captured[0].content.decode())
        assert body["exclude"] == ["10.0.0.1"]
