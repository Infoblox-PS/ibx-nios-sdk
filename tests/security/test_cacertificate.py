# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CacertificateResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.cacertificate import Cacertificate
from tests.conftest import json_response

WAPI_TYPE = "cacertificate"
REF = f"{WAPI_TYPE}/ZG5z:cert1"


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


async def test_cacertificate_list() -> None:
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
                        "distinguished_name": "CN=test",
                        "issuer": "CN=root",
                        "serial": "ABCD1234",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.cacertificate.list().all()
        assert len(records) == 1
        assert records[0].distinguished_name == "CN=test"
        assert captured[0].url.params["_paging"] == "1"


async def test_cacertificate_get() -> None:
    async with _client(
        _session_handler(
            {"_ref": REF, "distinguished_name": "CN=test", "issuer": "CN=root", "serial": "ABCD"}
        )
    ) as c:
        r = await c.security.cacertificate.get(REF)
        assert r.distinguished_name == "CN=test"
        assert r.issuer == "CN=root"


async def test_cacertificate_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "distinguished_name": "CN=test", "issuer": "CN=root"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.cacertificate.find_one(distinguished_name="CN=test")
        assert r is not None
        assert r.distinguished_name == "CN=test"


async def test_cacertificate_create() -> None:
    """cacertificate create - WapiResource.create available (all fields readOnly)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "distinguished_name": "CN=test"})

    async with _client(handler) as c:
        r = await c.security.cacertificate.create({})
        assert r.ref == REF
        req = captured[0]
        assert req.method == "POST"


async def test_cacertificate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = Cacertificate(
            **{
                "_ref": REF,
                "distinguished_name": "CN=test",
                "issuer": "CN=root",
                "serial": "ABCD",
                "uuid": "ro-uuid",
            }
        )
        await c.security.cacertificate.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"distinguished_name"' not in body, (
            "distinguished_name is readonly - must be stripped"
        )
        assert '"issuer"' not in body, "issuer is readonly - must be stripped"


async def test_cacertificate_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.cacertificate.delete(REF)
        assert result == REF
