# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TaxiiResource - list, get, find_one, update_strips_readonly, list_empty, paging."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.taxii import Taxii
from tests.conftest import json_response

WAPI_TYPE = "taxii"
REF = f"{WAPI_TYPE}/ZG5z:taxii1"


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


async def test_taxii_list() -> None:
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
                        "name": "taxii1",
                        "enable_service": True,
                        "ipv4addr": "10.0.0.1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.taxii.list().all()
        assert len(records) == 1
        assert records[0].name == "taxii1"
        assert captured[0].url.params["_paging"] == "1"


async def test_taxii_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "taxii1", "enable_service": True})
    ) as c:
        r = await c.misc.taxii.get(REF)
        assert r.name == "taxii1"
        assert r.ref == REF


async def test_taxii_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "taxii1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.taxii.find_one(name="taxii1")
        assert r is not None
        assert r.name == "taxii1"


async def test_taxii_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "enable_service": True})

    async with _client(handler) as c:
        obj = Taxii(
            **{
                "_ref": REF,
                "name": "taxii1",
                "ipv4addr": "10.0.0.1",
                "ipv6addr": "::1",
                "uuid": "ro-uuid",
                "enable_service": True,
            }
        )
        await c.misc.taxii.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"ipv4addr"' not in body, "ipv4addr is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"enable_service"' in body


async def test_taxii_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.taxii.list().all()
        assert records == []


async def test_taxii_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.taxii.list(max_results=5).all()
        assert captured[0].url.params["_max_results"] == "5"
