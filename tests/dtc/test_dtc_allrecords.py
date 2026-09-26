# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcAllrecordsResource - list, get, find_one, type_ alias, readonly check."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_allrecords import DtcAllrecords
from tests.conftest import json_response

WAPI_TYPE = "dtc:allrecords"
REF = f"{WAPI_TYPE}/ZG5z:allrec1"


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


async def test_dtc_allrecords_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "dtc_server": "srv1", "type": "A", "comment": "test"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.allrecords.list().all()
        assert len(records) == 1
        assert records[0].dtc_server == "srv1"
        assert records[0].type_ == "A"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_allrecords_get() -> None:
    async with _client(_session_handler({"_ref": REF, "dtc_server": "srv1", "type": "AAAA"})) as c:
        r = await c.dtc.allrecords.get(REF)
        assert r.type_ == "AAAA"
        assert r.dtc_server == "srv1"


async def test_dtc_allrecords_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "dtc_server": "srv1"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.allrecords.find_one()
        assert r is not None
        assert r.dtc_server == "srv1"


async def test_dtc_allrecords_type_alias() -> None:
    """type_ must deserialise from the 'type' JSON key."""
    obj = DtcAllrecords(**{"_ref": REF, "type": "CNAME", "dtc_server": "srv1"})
    assert obj.type_ == "CNAME"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert "type" in dumped
    assert dumped["type"] == "CNAME"


async def test_dtc_allrecords_readonly_fields_stripped_on_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF})

    async with _client(handler) as c:
        obj = DtcAllrecords(
            **{"_ref": REF, "dtc_server": "srv1", "type": "A", "comment": "ro", "ttl": 300}
        )
        await c.dtc.allrecords.update(REF, obj)
        body = captured[0].content.decode()
        assert '"dtc_server"' not in body
        assert '"comment"' not in body
        assert "300" in body  # ttl is writable


async def test_dtc_allrecords_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc_allrecords import DtcAllrecordsResource

    assert DtcAllrecordsResource._wapi_type == "dtc:allrecords"
