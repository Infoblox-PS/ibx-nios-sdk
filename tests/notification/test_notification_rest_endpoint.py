# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRestEndpointResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.notification.models.notification_rest_endpoint import NotificationRestEndpoint
from tests.conftest import json_response

WAPI_TYPE = "notification:rest:endpoint"
REF = f"{WAPI_TYPE}/ZG5z:ep1"


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


async def test_notification_rest_endpoint_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "ep1", "uri": "https://example.com/hook"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.notification.rest_endpoint.list().all()
        assert len(records) == 1
        assert records[0].name == "ep1"
        assert records[0].uri == "https://example.com/hook"
        assert captured[0].url.params["_paging"] == "1"


async def test_notification_rest_endpoint_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "ep1", "uri": "https://example.com/hook"})
    ) as c:
        r = await c.notification.rest_endpoint.get(REF)
        assert r.name == "ep1"
        assert r.ref == REF


async def test_notification_rest_endpoint_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "ep1"}], "next_page_id": ""})
    ) as c:
        r = await c.notification.rest_endpoint.find_one(name="ep1")
        assert r is not None
        assert r.name == "ep1"


async def test_notification_rest_endpoint_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "ep1"})

    async with _client(handler) as c:
        r = await c.notification.rest_endpoint.create(
            {"name": "ep1", "uri": "https://example.com/hook"}
        )
        assert r.name == "ep1"
        req = captured[0]
        assert req.method == "POST"
        assert '"ep1"' in req.content.decode()


async def test_notification_rest_endpoint_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "ep1"})

    async with _client(handler) as c:
        obj = NotificationRestEndpoint(
            **{
                "_ref": REF,
                "name": "ep1",
                "uuid": "ro-uuid",
                "client_certificate_subject": "CN=test",
            }
        )
        await c.notification.rest_endpoint.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"client_certificate_subject"' not in body, "readonly field must be stripped"
        assert '"ep1"' in body


async def test_notification_rest_endpoint_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.notification.rest_endpoint.delete(REF)
        assert result == REF
