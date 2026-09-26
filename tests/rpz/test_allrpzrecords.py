# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AllrpzrecordsResource - read-only aggregate: list, get, find_one, type_ alias, readonly fields."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.rpz.models.allrpzrecords import Allrpzrecords
from tests.conftest import json_response

WAPI_TYPE = "allrpzrecords"
REF = f"{WAPI_TYPE}/ZG5z:bad.rpz.example.com"


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


async def test_allrpzrecords_list() -> None:
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
                        "name": "bad.rpz.example.com",
                        "type": "record:rpz:cname",
                        "view": "default",
                        "zone": "rpz.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.rpz.allrpzrecords.list(zone="rpz.example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "bad.rpz.example.com"
        assert r.zone == "rpz.example.com"
        assert captured[0].url.params["zone"] == "rpz.example.com"


async def test_allrpzrecords_type_alias() -> None:
    """type field must be accessible as type_ (Python keyword workaround)."""
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "bad.rpz.example.com",
                        "type": "record:rpz:cname",
                        "view": "default",
                        "zone": "rpz.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        records = await c.rpz.allrpzrecords.list().all()
        assert len(records) == 1
        r = records[0]
        # type_ is the Python attribute; "type" is the wire alias
        assert r.type_ == "record:rpz:cname"


async def test_allrpzrecords_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "type": "record:rpz:a",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "blocked",
            }
        )
    ) as c:
        r = await c.rpz.allrpzrecords.get(REF)
        assert r.name == "bad.rpz.example.com"
        assert r.type_ == "record:rpz:a"
        assert r.comment == "blocked"


async def test_allrpzrecords_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "bad.rpz.example.com",
                        "type": "record:rpz:txt",
                        "view": "default",
                        "zone": "rpz.example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.rpz.allrpzrecords.find_one(name="bad.rpz.example.com")
        assert r is not None
        assert r.type_ == "record:rpz:txt"


async def test_allrpzrecords_model_roundtrip() -> None:
    """Allrpzrecords model validates all known read-only fields correctly."""
    data = {
        "_ref": REF,
        "name": "bad.rpz.example.com",
        "type": "record:rpz:cname",
        "view": "default",
        "zone": "rpz.example.com",
        "comment": "rpz blocked",
        "disable": True,
        "ttl": 3600,
        "rpz_rule": "GIVEN",
        "alert_type": "THREAT",
        "last_updated": 1700000000,
        "expiration_time": 0,
    }
    obj = Allrpzrecords.model_validate(data)
    assert obj.name == "bad.rpz.example.com"
    assert obj.type_ == "record:rpz:cname"
    assert obj.disable is True
    assert obj.ttl == 3600
    assert obj.rpz_rule == "GIVEN"


async def test_allrpzrecords_readonly_strip_on_update() -> None:
    """Update to allrpzrecords should strip all known readonly fields."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "bad.rpz.example.com",
                "type": "record:rpz:cname",
                "view": "default",
                "zone": "rpz.example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        obj = Allrpzrecords.model_validate(
            {
                "name": "bad.rpz.example.com",
                "type": "record:rpz:cname",
                "zone": "rpz.example.com",
                "view": "default",
                "comment": "",
            }
        )
        await c.rpz.allrpzrecords.update(REF, obj)
        body = captured[0].content.decode()
        # All allrpzrecords fields are readonly - body should only have non-stripped fields
        assert '"zone"' not in body
        assert '"name"' not in body
        assert '"type"' not in body
