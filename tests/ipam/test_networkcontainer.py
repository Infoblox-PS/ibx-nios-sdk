# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkcontainerResource - CRUD, find_one, list, extattrs, readonly-strip, next_available_network."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.networkcontainer import Networkcontainer
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns networkcontainer objects
# ---------------------------------------------------------------------------


async def test_networkcontainer_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "networkcontainer/ZG5z:10.0.0.0/8/default",
                        "network": "10.0.0.0/8",
                        "network_view": "default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        containers = await c.ipam.networkcontainer.list().all()
        assert len(containers) == 1
        nc = containers[0]
        assert nc.network == "10.0.0.0/8"
        assert nc.network_view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "network" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_networkcontainer_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "networkcontainer/ZG5z:10.0.0.0/8/default",
                        "network": "10.0.0.0/8",
                        "network_view": "default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        containers = await c.ipam.networkcontainer.list(network_view="default").all()
        assert len(containers) == 1

        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_networkcontainer_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "networkcontainer/ZG5z:10.0.0.0/8/default",
                "network": "10.0.0.0/8",
                "network_view": "default",
                "comment": "Main supernet",
            }
        )

    async with _client(handler) as c:
        ref = "networkcontainer/ZG5z:10.0.0.0/8/default"
        nc = await c.ipam.networkcontainer.get(ref)
        assert nc.network == "10.0.0.0/8"
        assert nc.comment == "Main supernet"


# ---------------------------------------------------------------------------
# 4. find_one(network="10.0.0.0/8") - returns first match
# ---------------------------------------------------------------------------


async def test_networkcontainer_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "networkcontainer/ZG5z:10.0.0.0/8/default",
                        "network": "10.0.0.0/8",
                        "network_view": "default",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        nc = await c.ipam.networkcontainer.find_one(network="10.0.0.0/8")
        assert nc is not None
        assert nc.network == "10.0.0.0/8"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_networkcontainer_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "networkcontainer/ZG5z:172.16.0.0/12/default",
                "network": "172.16.0.0/12",
                "network_view": "default",
                "comment": "RFC1918 supernet",
            }
        )

    async with _client(handler) as c:
        nc = await c.ipam.networkcontainer.create(
            {
                "network": "172.16.0.0/12",
                "network_view": "default",
                "comment": "RFC1918 supernet",
            }
        )
        assert nc.network == "172.16.0.0/12"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {...}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_networkcontainer_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "networkcontainer/ZG5z:10.0.0.0/8/default",
                "network": "10.0.0.0/8",
                "network_view": "default",
                "comment": "Updated",
            }
        )

    async with _client(handler) as c:
        ref = "networkcontainer/ZG5z:10.0.0.0/8/default"
        nc = await c.ipam.networkcontainer.update(ref, {"comment": "Updated"})
        assert nc.comment == "Updated"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path


# ---------------------------------------------------------------------------
# Extra: readonly-strip on update
# ---------------------------------------------------------------------------


async def test_networkcontainer_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "networkcontainer/ZG5z:10.0.0.0/8/default",
                "network": "10.0.0.0/8",
                "network_view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "networkcontainer/ZG5z:10.0.0.0/8/default"
        nc = Networkcontainer(
            network="10.0.0.0/8",
            comment="updated",
            utilization=50,  # RO
            uuid="some-uuid",  # RO
            rir="ARIN",  # RO
        )
        await c.ipam.networkcontainer.update(ref, nc)
        body = json.loads(captured[0].content.decode())

        assert "utilization" not in body, "utilization is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert "rir" not in body, "rir is readonly - must be stripped"
        assert body.get("comment") == "updated"


# ---------------------------------------------------------------------------
# Function call: next_available_network
# ---------------------------------------------------------------------------


async def test_networkcontainer_next_available_network() -> None:
    """POST to /{ref}?_function=next_available_network with body {"cidr": 26, "num": 2}."""
    captured: list[httpx.Request] = []
    expected_networks = ["10.0.0.0/26", "10.0.0.64/26"]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"networks": expected_networks})

    async with _client(handler) as c:
        ref = "networkcontainer/ZG5z:10.0.0.0/8/default"
        result = await c.ipam.networkcontainer.next_available_network(ref, cidr=26, num=2)

        assert result["networks"] == expected_networks

        req = captured[0]
        assert req.method == "POST"
        assert ref in req.url.path
        assert req.url.params.get("_function") == "next_available_network"

        body = json.loads(req.content.decode())
        assert body["cidr"] == 26
        assert body["num"] == 2
        assert "exclude" not in body


async def test_networkcontainer_next_available_network_with_exclude() -> None:
    """Passing exclude must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"networks": ["10.0.0.128/26"]})

    async with _client(handler) as c:
        ref = "networkcontainer/ZG5z:10.0.0.0/8/default"
        result = await c.ipam.networkcontainer.next_available_network(
            ref, cidr=26, num=1, exclude=["10.0.0.0/26"]
        )
        assert result["networks"] == ["10.0.0.128/26"]
        body = json.loads(captured[0].content.decode())
        assert body["exclude"] == ["10.0.0.0/26"]
