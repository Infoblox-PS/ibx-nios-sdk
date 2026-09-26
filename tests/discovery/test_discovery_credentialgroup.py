# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryCredentialgroupResource - list, get, find_one, create, update, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.discovery_credentialgroup import DiscoveryCredentialgroup
from tests.conftest import json_response

WAPI_TYPE = "discovery:credentialgroup"
REF = f"{WAPI_TYPE}/ZG5z:cg1"


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


async def test_discovery_credentialgroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF, "name": "cg1"}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.discovery.credentialgroup.list().all()
        assert len(records) == 1
        assert records[0].name == "cg1"
        assert captured[0].url.params["_paging"] == "1"


async def test_discovery_credentialgroup_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "cg1"})) as c:
        r = await c.discovery.credentialgroup.get(REF)
        assert r.name == "cg1"
        assert r.ref == REF


async def test_discovery_credentialgroup_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "cg1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.credentialgroup.find_one(name="cg1")
        assert r is not None
        assert r.name == "cg1"


async def test_discovery_credentialgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "cg1"})

    async with _client(handler) as c:
        r = await c.discovery.credentialgroup.create({"name": "cg1"})
        assert r.name == "cg1"
        assert captured[0].method == "POST"
        assert '"cg1"' in captured[0].content.decode()


async def test_discovery_credentialgroup_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "cg1"})

    async with _client(handler) as c:
        obj = DiscoveryCredentialgroup(**{"_ref": REF, "name": "cg1"})
        await c.discovery.credentialgroup.update(REF, obj)
        assert captured[0].method == "PUT"
        assert '"cg1"' in captured[0].content.decode()


async def test_discovery_credentialgroup_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.discovery.credentialgroup.delete(REF)
        assert result == REF
