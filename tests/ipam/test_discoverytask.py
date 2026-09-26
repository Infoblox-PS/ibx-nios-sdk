# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoverytaskResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.discoverytask import Discoverytask
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
# 1. list() - returns discoverytask objects
# ---------------------------------------------------------------------------


async def test_discoverytask_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "discoverytask/ZG5z:task1",
                        "status": "IDLE",
                        "network_view": "default",
                        "member_name": "grid.example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        tasks = await c.ipam.discovery_discoverytask.list().all()
        assert len(tasks) == 1
        t = tasks[0]
        assert t.network_view == "default"
        assert t.member_name == "grid.example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "status" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(network_view="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_discoverytask_list_by_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "discoverytask/ZG5z:task1",
                        "status": "IDLE",
                        "network_view": "default",
                        "member_name": "grid.example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        tasks = await c.ipam.discovery_discoverytask.list(network_view="default").all()
        assert len(tasks) == 1
        params = captured[0].url.params
        assert params.get("network_view") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_discoverytask_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "discoverytask/ZG5z:task1",
                "status": "RUNNING",
                "network_view": "default",
                "member_name": "grid.example.com",
                "mode": "FULL",
            }
        )

    async with _client(handler) as c:
        ref = "discoverytask/ZG5z:task1"
        t = await c.ipam.discovery_discoverytask.get(ref)
        assert t.status == "RUNNING"
        assert t.member_name == "grid.example.com"
        assert t.mode == "FULL"


# ---------------------------------------------------------------------------
# 4. find_one(member_name="grid.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_discoverytask_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "discoverytask/ZG5z:task1",
                        "status": "IDLE",
                        "network_view": "default",
                        "member_name": "grid.example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        t = await c.ipam.discovery_discoverytask.find_one(member_name="grid.example.com")
        assert t is not None
        assert t.member_name == "grid.example.com"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_discoverytask_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "discoverytask/ZG5z:task2",
                "status": "IDLE",
                "network_view": "test",
                "member_name": "member.example.com",
            }
        )

    async with _client(handler) as c:
        t = await c.ipam.discovery_discoverytask.create(
            {"network_view": "test", "member_name": "member.example.com"}
        )
        assert t.network_view == "test"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"member_name":"member.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (status, state, uuid, etc.)
# ---------------------------------------------------------------------------


async def test_discoverytask_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "discoverytask/ZG5z:task1",
                "status": "IDLE",
                "network_view": "default",
                "member_name": "grid.example.com",
            }
        )

    async with _client(handler) as c:
        ref = "discoverytask/ZG5z:task1"
        task = Discoverytask(
            member_name="grid.example.com",
            network_view="default",
            status="RUNNING",  # RO
            state="ACTIVE",  # RO
            uuid="some-uuid",  # RO
            warning="some warning",  # RO
        )
        await c.ipam.discovery_discoverytask.update(ref, task)
        body = json.loads(captured[0].content.decode())

        assert "status" not in body, "status is readonly - must be stripped"
        assert "state" not in body, "state is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert "warning" not in body, "warning is readonly - must be stripped"
        assert body.get("member_name") == "grid.example.com"
