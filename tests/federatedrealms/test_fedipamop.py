# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FedipamopResource - list, get, find_one, update (GET+PUT only, no POST/DELETE)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.federatedrealms.models.fedipamop import Fedipamop
from tests.conftest import json_response

WAPI_TYPE = "fedipamop"
REF = f"{WAPI_TYPE}/ZG5z:op1"


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


async def test_fedipamop_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.federatedrealms.fedipamop.list().all()
        assert len(records) == 1
        assert records[0].ref == REF
        assert captured[0].url.params["_paging"] == "1"


async def test_fedipamop_get() -> None:
    async with _client(_session_handler({"_ref": REF})) as c:
        r = await c.federatedrealms.fedipamop.get(REF)
        assert r.ref == REF


async def test_fedipamop_find_one() -> None:
    async with _client(_session_handler({"result": [{"_ref": REF}], "next_page_id": ""})) as c:
        r = await c.federatedrealms.fedipamop.find_one()
        assert r is not None
        assert r.ref == REF


async def test_fedipamop_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = Fedipamop(**{"_ref": REF, "get_ancestor_federated_realms": {"key": "val"}})
        await c.federatedrealms.fedipamop.update(REF, obj)
        req = captured[0]
        assert req.method == "PUT"
        assert "fedipamop" in req.url.path


async def test_fedipamop_model_fields() -> None:
    """Verify model fields are correct."""
    obj = Fedipamop(**{"_ref": REF, "get_ancestor_federated_realms": {"realms": []}})
    assert obj.ref == REF
    assert obj.get_ancestor_federated_realms == {"realms": []}


async def test_fedipamop_wapi_type() -> None:
    """Verify wapi_type is correct."""
    from ibx_nios_sdk.federatedrealms._fedipamop import FedipamopResource

    assert FedipamopResource._wapi_type == "fedipamop"
