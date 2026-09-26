# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ApprovalworkflowResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.approvalworkflow import Approvalworkflow
from tests.conftest import json_response

WAPI_TYPE = "approvalworkflow"
REF = f"{WAPI_TYPE}/ZG5z:wf1"


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


async def test_approvalworkflow_list() -> None:
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
                        "approval_group": "approvers",
                        "submitter_group": "submitters",
                        "ticket_number": "TICK-001",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.approvalworkflow.list().all()
        assert len(records) == 1
        assert records[0].approval_group == "approvers"
        assert captured[0].url.params["_paging"] == "1"


async def test_approvalworkflow_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "approval_group": "approvers",
                "ticket_number": "TICK-001",
            }
        )
    ) as c:
        r = await c.security.approvalworkflow.get(REF)
        assert r.approval_group == "approvers"
        assert r.ticket_number == "TICK-001"


async def test_approvalworkflow_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {"_ref": REF, "approval_group": "approvers", "ticket_number": "TICK-001"}
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.approvalworkflow.find_one(approval_group="approvers")
        assert r is not None
        assert r.approval_group == "approvers"


async def test_approvalworkflow_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": REF, "approval_group": "approvers", "ticket_number": "TICK-001"}
        )

    async with _client(handler) as c:
        r = await c.security.approvalworkflow.create(
            {"approval_group": "approvers", "ticket_number": "TICK-001"}
        )
        assert r.approval_group == "approvers"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"approvers"' in body


async def test_approvalworkflow_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "approval_group": "approvers"})

    async with _client(handler) as c:
        obj = Approvalworkflow(**{"_ref": REF, "approval_group": "approvers", "uuid": "ro-uuid"})
        await c.security.approvalworkflow.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"approvers"' in body


async def test_approvalworkflow_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.approvalworkflow.delete(REF)
        assert result == REF
