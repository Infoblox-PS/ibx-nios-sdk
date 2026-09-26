# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmEntrustnshieldgroupResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.hsm_entrustnshieldgroup import HsmEntrustnshieldgroup
from tests.conftest import json_response

WAPI_TYPE = "hsm:entrustnshieldgroup"
REF = f"{WAPI_TYPE}/ZG5z:entrust1"


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


async def test_hsm_entrustnshieldgroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "entrust-group-1", "comment": "HSM group"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.hsm_entrustnshieldgroup.list().all()
        assert len(records) == 1
        assert records[0].name == "entrust-group-1"
        assert captured[0].url.params["_paging"] == "1"


async def test_hsm_entrustnshieldgroup_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "entrust-group-1",
                "comment": "test",
                "status": "ACTIVE",
                "key_server_ip": "10.1.1.100",
            }
        )
    ) as c:
        r = await c.security.hsm_entrustnshieldgroup.get(REF)
        assert r.name == "entrust-group-1"
        assert r.status == "ACTIVE"
        assert r.key_server_ip == "10.1.1.100"


async def test_hsm_entrustnshieldgroup_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "entrust-group-1", "comment": ""}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.hsm_entrustnshieldgroup.find_one(name="entrust-group-1")
        assert r is not None
        assert r.name == "entrust-group-1"


async def test_hsm_entrustnshieldgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "entrust-group-1", "comment": "created"})

    async with _client(handler) as c:
        r = await c.security.hsm_entrustnshieldgroup.create(
            {"name": "entrust-group-1", "comment": "created"}
        )
        assert r.name == "entrust-group-1"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"entrust-group-1"' in body


async def test_hsm_entrustnshieldgroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "entrust-group-1", "comment": "updated"})

    async with _client(handler) as c:
        obj = HsmEntrustnshieldgroup(
            **{
                "_ref": REF,
                "name": "entrust-group-1",
                "comment": "updated",
                "status": "ACTIVE",
                "uuid": "ro-uuid",
            }
        )
        await c.security.hsm_entrustnshieldgroup.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"entrust-group-1"' in body


async def test_hsm_entrustnshieldgroup_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.hsm_entrustnshieldgroup.delete(REF)
        assert result == REF
