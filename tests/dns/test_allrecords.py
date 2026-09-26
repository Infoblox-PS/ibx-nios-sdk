# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AllrecordsResource - list, get, find_one, type_ alias, readonly-strip, delete.

Allrecords is a read-only aggregate; all non-_ref fields are readOnly in swagger.
create/update/delete exist on the resource but WAPI will reject them.
"""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.allrecords import Allrecords
from tests.conftest import json_response


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


# ---------------------------------------------------------------------------
# 1. list with filter
# ---------------------------------------------------------------------------


async def test_allrecords_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "allrecords/ZG5z:A/example.com/default",
                        "name": "host.example.com",
                        "type": "record:a",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.allrecords.list(view="default").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.type_ == "record:a"
        assert r.view == "default"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model
# ---------------------------------------------------------------------------


async def test_allrecords_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "allrecords/ZG5z:A/example.com/default",
                "name": "host.example.com",
                "type": "record:a",
                "view": "default",
                "zone": "example.com",
                "comment": "web server",
                "ttl": 300,
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "allrecords/ZG5z:A/example.com/default"
        r = await c.dns.allrecords.get(ref)
        assert r.name == "host.example.com"
        assert r.type_ == "record:a"
        assert r.view == "default"
        assert r.zone == "example.com"
        assert r.comment == "web server"
        assert r.ttl == 300
        assert r.disable is False


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_allrecords_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "allrecords/ZG5z:A/example.com/default",
                        "name": "host.example.com",
                        "type": "record:a",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.allrecords.find_one(name="host.example.com")
        assert r is not None
        assert r.name == "host.example.com"
        assert r.zone == "example.com"


# ---------------------------------------------------------------------------
# 4. type_ alias roundtrip
# ---------------------------------------------------------------------------


async def test_allrecords_type_alias_roundtrip() -> None:
    """Allrecords.type_ parses from 'type' key and serialises back correctly."""
    raw = {
        "_ref": "allrecords/ZG5z:CNAME/example.com/default",
        "name": "alias.example.com",
        "type": "record:cname",
        "view": "default",
        "zone": "example.com",
        "comment": "",
    }
    obj = Allrecords.model_validate(raw)
    assert obj.type_ == "record:cname"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert dumped["type"] == "record:cname"
    assert "type_" not in dumped


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_allrecords_update_strips_readonly() -> None:
    """All non-ref fields are read-only; none should appear in a PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "allrecords/ZG5z:A/example.com/default",
                "name": "host.example.com",
                "type": "record:a",
            }
        )

    async with _client(handler) as c:
        ref = "allrecords/ZG5z:A/example.com/default"
        r = Allrecords(
            **{
                "_ref": ref,
                "name": "host.example.com",
                "type": "record:a",
                "view": "default",
                "zone": "example.com",
                "comment": "note",
                "ttl": 300,
            }
        )
        await c.dns.allrecords.update(ref, r)
        body = captured[0].content.decode()
        # All payload fields are in READONLY_FIELDS - should be stripped
        assert '"name"' not in body
        assert '"type"' not in body
        assert '"view"' not in body
        assert '"zone"' not in body
        assert '"comment"' not in body
        assert '"ttl"' not in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_allrecords_delete() -> None:
    """delete() returns the ref string (WAPI would 400 in reality; SDK allows it)."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("allrecords/ZG5z:A/example.com/default")

    async with _client(handler) as c:
        result = await c.dns.allrecords.delete("allrecords/ZG5z:A/example.com/default")
        assert result == "allrecords/ZG5z:A/example.com/default"
