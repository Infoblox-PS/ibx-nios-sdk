# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TacacsplusAuthserviceResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.tacacsplus_authservice import TacacsplusAuthservice
from tests.conftest import json_response

WAPI_TYPE = "tacacsplus:authservice"
REF = f"{WAPI_TYPE}/ZG5z:tacacs1"


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


async def test_tacacsplus_authservice_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "tacacs-svc", "comment": "tacacs"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.tacacsplus_authservice.list().all()
        assert len(records) == 1
        assert records[0].name == "tacacs-svc"
        assert captured[0].url.params["_paging"] == "1"


async def test_tacacsplus_authservice_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "tacacs-svc", "comment": "test"})
    ) as c:
        r = await c.security.tacacsplus_authservice.get(REF)
        assert r.name == "tacacs-svc"


async def test_tacacsplus_authservice_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "tacacs-svc", "comment": ""}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.tacacsplus_authservice.find_one(name="tacacs-svc")
        assert r is not None
        assert r.name == "tacacs-svc"


async def test_tacacsplus_authservice_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "tacacs-svc", "comment": "created"})

    async with _client(handler) as c:
        r = await c.security.tacacsplus_authservice.create(
            {"name": "tacacs-svc", "comment": "created"}
        )
        assert r.name == "tacacs-svc"
        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"tacacs-svc"' in body


async def test_tacacsplus_authservice_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "tacacs-svc", "comment": "updated"})

    async with _client(handler) as c:
        obj = TacacsplusAuthservice(
            **{"_ref": REF, "name": "tacacs-svc", "comment": "updated", "uuid": "ro-uuid"}
        )
        await c.security.tacacsplus_authservice.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"tacacs-svc"' in body


async def test_tacacsplus_authservice_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.tacacsplus_authservice.delete(REF)
        assert result == REF
