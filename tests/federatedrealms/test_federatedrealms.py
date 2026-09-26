# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FederatedrealmsResource - list, get, find_one (read-only, no POST/PUT/DELETE)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "federatedrealms"
REF = f"{WAPI_TYPE}/ZG5z:realm1"


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


async def test_federatedrealms_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "id": "realm-id-1", "name": "realm1"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.federatedrealms.federatedrealms.list().all()
        assert len(records) == 1
        assert records[0].name == "realm1"
        assert records[0].id == "realm-id-1"
        assert captured[0].url.params["_paging"] == "1"


async def test_federatedrealms_get() -> None:
    async with _client(_session_handler({"_ref": REF, "id": "realm-id-1", "name": "realm1"})) as c:
        r = await c.federatedrealms.federatedrealms.get(REF)
        assert r.name == "realm1"
        assert r.id == "realm-id-1"
        assert r.ref == REF


async def test_federatedrealms_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "id": "realm-id-1", "name": "realm1"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.federatedrealms.federatedrealms.find_one(name="realm1")
        assert r is not None
        assert r.name == "realm1"


async def test_federatedrealms_model_fields() -> None:
    """Verify model fields are correct."""
    from ibx_nios_sdk.federatedrealms.models.federatedrealms import Federatedrealms

    obj = Federatedrealms(**{"_ref": REF, "id": "realm-id-1", "name": "realm1"})
    assert obj.ref == REF
    assert obj.id == "realm-id-1"
    assert obj.name == "realm1"


async def test_federatedrealms_wapi_type() -> None:
    """Verify wapi_type is correct."""
    from ibx_nios_sdk.federatedrealms._federatedrealms import FederatedrealmsResource

    assert FederatedrealmsResource._wapi_type == "federatedrealms"


async def test_federatedrealms_readonly_fields() -> None:
    """Readonly fields should include id and name."""
    from ibx_nios_sdk.federatedrealms.models.federatedrealms import READONLY_FIELDS

    assert "id" in READONLY_FIELDS
    assert "name" in READONLY_FIELDS
