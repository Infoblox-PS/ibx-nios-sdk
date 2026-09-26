# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcResource - list, get, find_one, update, and wapi_type checks."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc import Dtc
from tests.conftest import json_response

WAPI_TYPE = "dtc"
REF = f"{WAPI_TYPE}/ZG5z:dtc"


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


async def test_dtc_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.dtc.dtc.list().all()
        assert len(records) == 1
        assert records[0].ref == REF
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_get() -> None:
    async with _client(_session_handler({"_ref": REF})) as c:
        r = await c.dtc.dtc.get(REF)
        assert r.ref == REF


async def test_dtc_find_one() -> None:
    async with _client(_session_handler({"result": [{"_ref": REF}], "next_page_id": ""})) as c:
        r = await c.dtc.dtc.find_one()
        assert r is not None
        assert r.ref == REF


async def test_dtc_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        r = await c.dtc.dtc.update(REF, {"query": {"type": "A"}})
        assert r.ref == REF
        assert captured[0].method == "PUT"


async def test_dtc_model_parses_fields() -> None:
    obj = Dtc(**{"_ref": REF, "query": {"type": "A"}})
    assert obj.ref == REF
    assert obj.query == {"type": "A"}


async def test_dtc_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc import DtcResource

    assert DtcResource._wapi_type == "dtc"
