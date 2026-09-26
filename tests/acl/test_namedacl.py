# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NamedaclResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.acl.models.namedacl import Namedacl
from tests.conftest import json_response

WAPI_TYPE = "namedacl"
REF = f"{WAPI_TYPE}/ZG5z:my-acl"


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


async def test_namedacl_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "name": "my-acl", "comment": "test acl"},
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.acl.namedacl.list().all()
        assert len(records) == 1
        assert records[0].name == "my-acl"
        params = captured[0].url.params
        assert params["_paging"] == "1"


async def test_namedacl_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "my-acl", "comment": "test"})) as c:
        r = await c.acl.namedacl.get(REF)
        assert r.name == "my-acl"
        assert r.ref == REF


async def test_namedacl_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "my-acl", "comment": ""}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.acl.namedacl.find_one(name="my-acl")
        assert r is not None
        assert r.name == "my-acl"


async def test_namedacl_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "my-acl", "comment": "created"})

    async with _client(handler) as c:
        r = await c.acl.namedacl.create({"name": "my-acl", "comment": "created"})
        assert r.name == "my-acl"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"
        body = req.content.decode()
        assert '"my-acl"' in body


async def test_namedacl_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "my-acl", "comment": "updated"})

    async with _client(handler) as c:
        obj = Namedacl(
            **{
                "_ref": REF,
                "name": "my-acl",
                "comment": "updated",
                "uuid": "ro-uuid",
                "exploded_access_list": [{"address": "any", "permission": "ALLOW"}],
            }
        )
        await c.acl.namedacl.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"exploded_access_list"' not in body, (
            "exploded_access_list is readonly - must be stripped"
        )
        assert '"my-acl"' in body


async def test_namedacl_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.acl.namedacl.delete(REF)
        assert result == REF
