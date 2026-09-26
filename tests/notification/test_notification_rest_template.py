# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRestTemplateResource - list, get, find_one, update_strips_readonly, delete (no POST)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.notification.models.notification_rest_template import NotificationRestTemplate
from tests.conftest import json_response

WAPI_TYPE = "notification:rest:template"
REF = f"{WAPI_TYPE}/ZG5z:tmpl1"


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


async def test_notification_rest_template_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "tmpl1", "outbound_type": "REST"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.notification.rest_template.list().all()
        assert len(records) == 1
        assert records[0].name == "tmpl1"
        assert records[0].outbound_type == "REST"
        assert captured[0].url.params["_paging"] == "1"


async def test_notification_rest_template_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "tmpl1", "outbound_type": "REST"})
    ) as c:
        r = await c.notification.rest_template.get(REF)
        assert r.name == "tmpl1"
        assert r.ref == REF


async def test_notification_rest_template_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "tmpl1"}], "next_page_id": ""})
    ) as c:
        r = await c.notification.rest_template.find_one(name="tmpl1")
        assert r is not None
        assert r.name == "tmpl1"


async def test_notification_rest_template_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "tmpl1"})

    async with _client(handler) as c:
        r = await c.notification.rest_template.update(REF, {"name": "tmpl1", "comment": "updated"})
        assert r.name == "tmpl1"
        req = captured[0]
        assert req.method == "PUT"


async def test_notification_rest_template_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "tmpl1"})

    async with _client(handler) as c:
        obj = NotificationRestTemplate(
            **{
                "_ref": REF,
                "name": "tmpl1",
                "uuid": "ro-uuid",
                "outbound_type": "REST",
                "action_name": "ro-action",
            }
        )
        await c.notification.rest_template.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"outbound_type"' not in body, "outbound_type is readonly - must be stripped"
        assert '"action_name"' not in body, "action_name is readonly - must be stripped"
        assert '"tmpl1"' in body


async def test_notification_rest_template_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.notification.rest_template.delete(REF)
        assert result == REF
