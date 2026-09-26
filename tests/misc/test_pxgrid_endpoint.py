# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""PxgridEndpointResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.misc.models.pxgrid_endpoint import PxgridEndpoint
from tests.conftest import json_response

WAPI_TYPE = "pxgrid:endpoint"
REF = f"{WAPI_TYPE}/ZG5z:pxg1"


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


async def test_pxgrid_endpoint_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "name": "pxg1", "comment": "PXGrid ep", "address": "10.0.0.2"}
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.misc.pxgrid_endpoint.list().all()
        assert len(records) == 1
        assert records[0].name == "pxg1"
        assert captured[0].url.params["_paging"] == "1"


async def test_pxgrid_endpoint_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "pxg1", "address": "10.0.0.2"})
    ) as c:
        r = await c.misc.pxgrid_endpoint.get(REF)
        assert r.name == "pxg1"
        assert r.ref == REF


async def test_pxgrid_endpoint_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "pxg1"}], "next_page_id": ""})
    ) as c:
        r = await c.misc.pxgrid_endpoint.find_one(name="pxg1")
        assert r is not None
        assert r.name == "pxg1"


async def test_pxgrid_endpoint_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "pxg1"})

    async with _client(handler) as c:
        r = await c.misc.pxgrid_endpoint.create({"name": "pxg1", "address": "10.0.0.2"})
        assert r.name == "pxg1"
        req = captured[0]
        assert req.method == "POST"
        assert '"pxg1"' in req.content.decode()


async def test_pxgrid_endpoint_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "pxg1"})

    async with _client(handler) as c:
        obj = PxgridEndpoint(
            **{
                "_ref": REF,
                "name": "pxg1",
                "uuid": "ro-uuid",
                "client_certificate_subject": "cn=test",
                "client_certificate_valid_from": 1000,
                "client_certificate_valid_to": 2000,
            }
        )
        await c.misc.pxgrid_endpoint.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"client_certificate_subject"' not in body
        assert '"pxg1"' in body


async def test_pxgrid_endpoint_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.misc.pxgrid_endpoint.delete(REF)
        assert result == REF
