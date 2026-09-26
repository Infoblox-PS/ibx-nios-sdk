# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRuleResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.notification.models.notification_rule import NotificationRule
from tests.conftest import json_response

WAPI_TYPE = "notification:rule"
REF = f"{WAPI_TYPE}/ZG5z:rule1"


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


async def test_notification_rule_list() -> None:
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
                        "name": "rule1",
                        "event_type": "DHCP_LEASE",
                        "notification_action": "SEND_EMAIL",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.notification.rule.list().all()
        assert len(records) == 1
        assert records[0].name == "rule1"
        assert records[0].event_type == "DHCP_LEASE"
        assert captured[0].url.params["_paging"] == "1"


async def test_notification_rule_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "rule1",
                "event_type": "DHCP_LEASE",
                "notification_action": "SEND_EMAIL",
            }
        )
    ) as c:
        r = await c.notification.rule.get(REF)
        assert r.name == "rule1"
        assert r.ref == REF


async def test_notification_rule_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "rule1"}], "next_page_id": ""})
    ) as c:
        r = await c.notification.rule.find_one(name="rule1")
        assert r is not None
        assert r.name == "rule1"


async def test_notification_rule_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "rule1"})

    async with _client(handler) as c:
        r = await c.notification.rule.create(
            {"name": "rule1", "event_type": "DHCP_LEASE", "notification_action": "SEND_EMAIL"}
        )
        assert r.name == "rule1"
        req = captured[0]
        assert req.method == "POST"
        assert '"rule1"' in req.content.decode()


async def test_notification_rule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "rule1"})

    async with _client(handler) as c:
        obj = NotificationRule(
            **{"_ref": REF, "name": "rule1", "uuid": "ro-uuid", "comment": "updated"}
        )
        await c.notification.rule.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"name"' not in body, (
            "name is create-only on notification:rule - stripped on update"
        )
        assert '"updated"' in body


async def test_notification_rule_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.notification.rule.delete(REF)
        assert result == REF
