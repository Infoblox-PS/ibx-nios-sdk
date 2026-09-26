# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RirResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.rir import Rir
from tests.conftest import json_response

WAPI_TYPE = "rir"
REF = f"{WAPI_TYPE}/ZG5z:RIPE"


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


async def test_rir_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.ipam.rir._wapi_type == WAPI_TYPE


async def test_rir_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "RIPE",
                        "communication_mode": "EMAIL",
                        "email": "ripe@example.com",
                        "url": "https://ripe.example.com",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        rirs = await c.ipam.rir.list().all()
        assert len(rirs) == 1
        assert rirs[0].name == "RIPE"
        assert rirs[0].email == "ripe@example.com"


async def test_rir_get_by_ref() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "RIPE",
                "communication_mode": "API",
                "url": "https://ripe.example.com",
            }
        )
    ) as c:
        r = await c.ipam.rir.get(REF)
        assert r.ref == REF
        assert r.communication_mode == "API"


async def test_rir_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "RIPE"}], "next_page_id": ""})
    ) as c:
        r = await c.ipam.rir.find_one(name="RIPE")
        assert r is not None
        assert r.name == "RIPE"


async def test_rir_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "RIPE"})

    async with _client(handler) as c:
        r = await c.ipam.rir.create({"name": "RIPE", "email": "ripe@example.com"})
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"RIPE"' in body
        assert '"ripe@example.com"' in body


async def test_rir_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "RIPE"})

    async with _client(handler) as c:
        obj = Rir(
            name="RIPE",
            email="ripe@example.com",
            communication_mode="EMAIL",
            uuid="ro-uuid",
        )
        await c.ipam.rir.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"email":"ripe@example.com"' in body


async def test_rir_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.ipam.rir.delete(REF) == REF
