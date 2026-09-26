# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ScheduledtaskResource - list, get, find_one, update_strips_readonly, delete, paging."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.scheduledtask import Scheduledtask
from tests.conftest import json_response

WAPI_TYPE = "scheduledtask"
REF = f"{WAPI_TYPE}/ZG5z:task1"


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


async def test_scheduledtask_list() -> None:
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
                        "task_id": 1,
                        "task_type": "CHANGE",
                        "execution_status": "PENDING",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.scheduledtask.list().all()
        assert len(records) == 1
        assert records[0].task_type == "CHANGE"
        assert records[0].execution_status == "PENDING"
        assert captured[0].url.params["_paging"] == "1"


async def test_scheduledtask_get() -> None:
    async with _client(_session_handler({"_ref": REF, "task_id": 1, "task_type": "CHANGE"})) as c:
        r = await c.misc.scheduledtask.get(REF)
        assert r.task_type == "CHANGE"
        assert r.ref == REF


async def test_scheduledtask_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "task_id": 1, "task_type": "CHANGE"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.misc.scheduledtask.find_one(task_type="CHANGE")
        assert r is not None
        assert r.task_type == "CHANGE"


async def test_scheduledtask_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "approval_status": "APPROVED"})

    async with _client(handler) as c:
        obj = Scheduledtask(
            **{
                "_ref": REF,
                "approval_status": "APPROVED",
                "approver_comment": "ok",
                "task_id": 1,
                "task_type": "CHANGE",
                "execution_status": "PENDING",
                "uuid": "ro-uuid",
            }
        )
        await c.misc.scheduledtask.update(REF, obj)
        body = captured[0].content.decode()
        assert '"task_id"' not in body, "task_id is readonly - must be stripped"
        assert '"task_type"' not in body, "task_type is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"APPROVED"' in body


async def test_scheduledtask_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.scheduledtask.delete(REF)
        assert result == REF


async def test_scheduledtask_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.scheduledtask.list(max_results=30).all()
        assert captured[0].url.params["_max_results"] == "30"
