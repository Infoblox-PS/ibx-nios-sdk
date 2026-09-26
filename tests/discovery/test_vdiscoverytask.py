# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VdiscoverytaskResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.discovery.models.vdiscoverytask import Vdiscoverytask
from tests.conftest import json_response

WAPI_TYPE = "vdiscoverytask"
REF = f"{WAPI_TYPE}/ZG5z:vdt1"


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


async def test_vdiscoverytask_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "vdt1", "driver_type": "VMWARE"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.discovery.vdiscoverytask.list().all()
        assert len(records) == 1
        assert records[0].name == "vdt1"
        assert records[0].driver_type == "VMWARE"
        assert captured[0].url.params["_paging"] == "1"


async def test_vdiscoverytask_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "vdt1", "state": "COMPLETED"})) as c:
        r = await c.discovery.vdiscoverytask.get(REF)
        assert r.name == "vdt1"
        assert r.state == "COMPLETED"


async def test_vdiscoverytask_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "vdt1"}], "next_page_id": ""})
    ) as c:
        r = await c.discovery.vdiscoverytask.find_one(name="vdt1")
        assert r is not None
        assert r.name == "vdt1"


async def test_vdiscoverytask_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "vdt1"})

    async with _client(handler) as c:
        r = await c.discovery.vdiscoverytask.create({"name": "vdt1", "driver_type": "VMWARE"})
        assert r.name == "vdt1"
        req = captured[0]
        assert req.method == "POST"
        assert '"vdt1"' in req.content.decode()


async def test_vdiscoverytask_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "vdt1"})

    async with _client(handler) as c:
        obj = Vdiscoverytask(
            **{
                "_ref": REF,
                "name": "vdt1",
                "state": "COMPLETED",
                "state_msg": "done",
                "last_run": 1700000000,
                "uuid": "ro-uuid",
                "enabled": True,
            }
        )
        await c.discovery.vdiscoverytask.update(REF, obj)
        body = captured[0].content.decode()
        assert '"state"' not in body, "state is readonly - must be stripped"
        assert '"state_msg"' not in body, "state_msg is readonly - must be stripped"
        assert '"last_run"' not in body, "last_run is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"vdt1"' in body


async def test_vdiscoverytask_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.discovery.vdiscoverytask.delete(REF)
        assert result == REF
