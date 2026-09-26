# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DatacollectionclusterResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.datacollectioncluster import Datacollectioncluster
from tests.conftest import json_response

WAPI_TYPE = "datacollectioncluster"
REF = f"{WAPI_TYPE}/ZG5z:dc1"


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


async def test_datacollectioncluster_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "dc1", "enable_registration": True}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.datacollectioncluster.list().all()
        assert len(records) == 1
        assert records[0].name == "dc1"
        assert captured[0].url.params["_paging"] == "1"


async def test_datacollectioncluster_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "dc1", "enable_registration": True})
    ) as c:
        r = await c.misc.datacollectioncluster.get(REF)
        assert r.name == "dc1"
        assert r.ref == REF


async def test_datacollectioncluster_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "dc1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.datacollectioncluster.find_one(name="dc1")
        assert r is not None
        assert r.name == "dc1"


async def test_datacollectioncluster_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "dc1"})

    async with _client(handler) as c:
        r = await c.misc.datacollectioncluster.create({"enable_registration": True})
        assert r.ref == REF
        req = captured[0]
        assert req.method == "POST"


async def test_datacollectioncluster_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "enable_registration": True})

    async with _client(handler) as c:
        obj = Datacollectioncluster(
            **{"_ref": REF, "name": "dc1", "uuid": "ro-uuid", "enable_registration": True}
        )
        await c.misc.datacollectioncluster.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"


async def test_datacollectioncluster_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.datacollectioncluster.delete(REF)
        assert result == REF
