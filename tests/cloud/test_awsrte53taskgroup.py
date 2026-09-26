# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Awsrte53taskgroupResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.cloud.models.awsrte53taskgroup import Awsrte53taskgroup
from tests.conftest import json_response

WAPI_TYPE = "awsrte53taskgroup"
REF = f"{WAPI_TYPE}/ZG5z:group1"


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


async def test_awsrte53taskgroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "name": "grp1", "comment": "test"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.cloud.awsrte53taskgroup.list().all()
        assert len(records) == 1
        assert records[0].name == "grp1"
        assert captured[0].url.params["_paging"] == "1"


async def test_awsrte53taskgroup_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "grp1"})) as c:
        r = await c.cloud.awsrte53taskgroup.get(REF)
        assert r.name == "grp1"
        assert r.ref == REF


async def test_awsrte53taskgroup_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "grp1"}], "next_page_id": ""})
    ) as c:
        r = await c.cloud.awsrte53taskgroup.find_one(name="grp1")
        assert r is not None
        assert r.name == "grp1"


async def test_awsrte53taskgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "grp1"})

    async with _client(handler) as c:
        r = await c.cloud.awsrte53taskgroup.create({"name": "grp1"})
        assert r.name == "grp1"
        req = captured[0]
        assert req.method == "POST"
        assert '"grp1"' in req.content.decode()


async def test_awsrte53taskgroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "grp1"})

    async with _client(handler) as c:
        obj = Awsrte53taskgroup(
            **{"_ref": REF, "name": "grp1", "uuid": "ro-uuid", "sync_status": "COMPLETED"}
        )
        await c.cloud.awsrte53taskgroup.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"sync_status"' not in body, "sync_status is readonly - must be stripped"
        assert '"grp1"' in body


async def test_awsrte53taskgroup_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.cloud.awsrte53taskgroup.delete(REF)
        assert result == REF
