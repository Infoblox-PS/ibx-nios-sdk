# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcObjectResource - list, get, find_one, update (GET+PUT, mostly read-only)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_object import DtcObject
from tests.conftest import json_response

WAPI_TYPE = "dtc:object"
REF = f"{WAPI_TYPE}/ZG5z:obj1"


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


async def test_dtc_object_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {"_ref": REF, "name": "obj1", "display_type": "DTC:SERVER", "status": "ONLINE"}
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.object.list().all()
        assert len(records) == 1
        assert records[0].name == "obj1"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_object_get() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "obj1", "status": "ONLINE"})) as c:
        r = await c.dtc.object.get(REF)
        assert r.name == "obj1"
        assert r.status == "ONLINE"


async def test_dtc_object_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "obj1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.object.find_one()
        assert r is not None
        assert r.name == "obj1"


async def test_dtc_object_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DtcObject(**{"_ref": REF, "name": "obj1", "status": "ONLINE", "comment": "readonly"})
        await c.dtc.object.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"status"' not in body, "status is readonly - must be stripped"
        assert '"comment"' not in body, "comment is readonly - must be stripped"


async def test_dtc_object_model_fields() -> None:
    obj = DtcObject(
        **{
            "_ref": REF,
            "name": "obj1",
            "display_type": "DTC:SERVER",
            "abstract_type": "SERVER",
            "status": "ONLINE",
            "ipv4_address_list": ["1.2.3.4"],
        }
    )
    assert obj.name == "obj1"
    assert obj.ipv4_address_list == ["1.2.3.4"]


async def test_dtc_object_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc_object import DtcObjectResource

    assert DtcObjectResource._wapi_type == "dtc:object"
