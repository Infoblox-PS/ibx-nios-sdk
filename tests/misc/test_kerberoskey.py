# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""KerberoskeyResource - list, get, find_one, delete (GET+DELETE only)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "kerberoskey"
REF = f"{WAPI_TYPE}/ZG5z:key1"


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


async def test_kerberoskey_list() -> None:
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
                        "principal": "host/example.com",
                        "domain": "EXAMPLE.COM",
                        "enctype": "AES256",
                        "version": 3,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.kerberoskey.list().all()
        assert len(records) == 1
        assert records[0].principal == "host/example.com"
        assert records[0].domain == "EXAMPLE.COM"
        assert captured[0].url.params["_paging"] == "1"


async def test_kerberoskey_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "principal": "host/example.com", "domain": "EXAMPLE.COM"})
    ) as c:
        r = await c.misc.kerberoskey.get(REF)
        assert r.principal == "host/example.com"
        assert r.ref == REF


async def test_kerberoskey_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "principal": "host/example.com"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.misc.kerberoskey.find_one(principal="host/example.com")
        assert r is not None
        assert r.principal == "host/example.com"


async def test_kerberoskey_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.kerberoskey.delete(REF)
        assert result == REF


async def test_kerberoskey_list_empty() -> None:
    async with _client(_session_handler({"result": [], "next_page_id": ""})) as c:
        records = await c.misc.kerberoskey.list().all()
        assert records == []


async def test_kerberoskey_list_paging_params() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    async with _client(handler) as c:
        await c.misc.kerberoskey.list(max_results=50).all()
        assert captured[0].url.params["_max_results"] == "50"
