# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_topology import DtcTopology
from tests.conftest import json_response

WAPI_TYPE = "dtc:topology"
REF = f"{WAPI_TYPE}/ZG5z:topo1"


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


async def test_dtc_topology_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "topo1", "comment": "test"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.topology.list().all()
        assert len(records) == 1
        assert records[0].name == "topo1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_topology_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "topo1", "comment": "test"})) as c:
        r = await c.dtc.topology.get(REF)
        assert r.name == "topo1"


async def test_dtc_topology_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "topo1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.topology.find_one(name="topo1")
        assert r is not None
        assert r.name == "topo1"


async def test_dtc_topology_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "topo1"})

    async with _client(handler) as c:
        r = await c.dtc.topology.create({"name": "topo1"})
        assert r.name == "topo1"
        assert captured[0].method == "POST"


async def test_dtc_topology_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "topo1"})

    async with _client(handler) as c:
        obj = DtcTopology(**{"_ref": REF, "name": "topo1", "uuid": "ro-uuid"})
        await c.dtc.topology.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"topo1"' in body


async def test_dtc_topology_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.dtc.topology.delete(REF)
        assert result == REF
