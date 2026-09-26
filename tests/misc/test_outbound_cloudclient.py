# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""OutboundCloudclientResource - list, get, find_one, update_strips_readonly, list_empty, paging."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.outbound_cloudclient import OutboundCloudclient
from tests.conftest import json_response

WAPI_TYPE = "outbound:cloudclient"
REF = f"{WAPI_TYPE}/ZG5z:occ1"


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


async def test_outbound_cloudclient_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": REF,
                        "grid_member": "infoblox.localdomain",
                        "enable": True,
                        "interval": 60,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.outbound_cloudclient.list().all()
        assert len(records) == 1
        assert records[0].grid_member == "infoblox.localdomain"
        assert captured[0].url.params["_paging"] == "1"


async def test_outbound_cloudclient_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "grid_member": "infoblox.localdomain", "enable": True})
    ) as c:
        r = await c.misc.outbound_cloudclient.get(REF)
        assert r.grid_member == "infoblox.localdomain"
        assert r.ref == REF


async def test_outbound_cloudclient_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "grid_member": "infoblox.localdomain"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.misc.outbound_cloudclient.find_one(grid_member="infoblox.localdomain")
        assert r is not None
        assert r.grid_member == "infoblox.localdomain"


async def test_outbound_cloudclient_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "enable": True})

    async with _client(handler) as c:
        obj = OutboundCloudclient(**{"_ref": REF, "enable": True, "uuid": "ro-uuid"})
        await c.misc.outbound_cloudclient.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"enable"' in body


async def test_outbound_cloudclient_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.outbound_cloudclient.list().all()
        assert records == []


async def test_outbound_cloudclient_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.outbound_cloudclient.list(max_results=10).all()
        assert captured[0].url.params["_max_results"] == "10"
