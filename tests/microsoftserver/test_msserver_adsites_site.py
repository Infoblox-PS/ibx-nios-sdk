# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverAdsitesSiteResource - list, get, find_one, create, update, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.microsoftserver.models.msserver_adsites_site import MsserverAdsitesSite
from tests.conftest import json_response

WAPI_TYPE = "msserver:adsites:site"
REF = f"{WAPI_TYPE}/ZG5z:site1"


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


async def test_msserver_adsites_site_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "Site1", "domain": "corp.com"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.microsoftserver.adsites_site.list().all()
        assert len(records) == 1
        assert records[0].name == "Site1"
        assert records[0].domain == "corp.com"
        assert captured[0].url.params["_paging"] == "1"


async def test_msserver_adsites_site_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "Site1", "domain": "corp.com"})
    ) as c:
        r = await c.microsoftserver.adsites_site.get(REF)
        assert r.name == "Site1"
        assert r.domain == "corp.com"


async def test_msserver_adsites_site_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "Site1"}], "next_page_id": ""})
    ) as c:
        r = await c.microsoftserver.adsites_site.find_one(name="Site1")
        assert r is not None
        assert r.name == "Site1"


async def test_msserver_adsites_site_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "Site1"})

    async with _client(handler) as c:
        r = await c.microsoftserver.adsites_site.create({"name": "Site1", "domain": "corp.com"})
        assert r.name == "Site1"
        assert captured[0].method == "POST"
        assert '"Site1"' in captured[0].content.decode()


async def test_msserver_adsites_site_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = MsserverAdsitesSite(**{"_ref": REF, "name": "Site1", "domain": "corp.com"})
        await c.microsoftserver.adsites_site.update(REF, obj)
        body = captured[0].content.decode()
        assert '"Site1"' in body
        assert captured[0].method == "PUT"


async def test_msserver_adsites_site_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.microsoftserver.adsites_site.delete(REF)
        assert result == REF
