# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AllnsgroupResource - list, get, find_one, and type_ alias.

Allnsgroup is a read-only aggregate; create/update/delete exist on the resource
but WAPI will reject them.  The test suite covers the three read operations and
verifies the ``type_`` alias works correctly.
"""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.allnsgroup import Allnsgroup
from tests.conftest import json_response


def _client(handler) -> NiosClient:
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


async def test_allnsgroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "allnsgroup/ZG5z:default",
                        "name": "default",
                        "type": "nsgroup",
                    },
                    {
                        "_ref": "allnsgroup/ZG5z:deleggrp",
                        "name": "deleggrp",
                        "type": "nsgroup:delegation",
                    },
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.allnsgroup.list().all()
        assert len(groups) == 2
        assert groups[0].name == "default"
        assert groups[0].type_ == "nsgroup"
        assert groups[1].type_ == "nsgroup:delegation"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


async def test_allnsgroup_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "allnsgroup/ZG5z:default",
                "name": "default",
                "type": "nsgroup",
                "comment": "grid default NS group",
            }
        )

    async with _client(handler) as c:
        ref = "allnsgroup/ZG5z:default"
        g = await c.dns.allnsgroup.get(ref)
        assert g.name == "default"
        assert g.type_ == "nsgroup"
        assert g.comment == "grid default NS group"


async def test_allnsgroup_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {"_ref": "allnsgroup/ZG5z:default", "name": "default", "type": "nsgroup"}
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.allnsgroup.find_one(name="default")
        assert g is not None
        assert g.name == "default"


async def test_allnsgroup_type_alias_roundtrip() -> None:
    """Allnsgroup.type_ parses from 'type' key and serialises back correctly."""
    raw = {"_ref": "allnsgroup/ZG5z:x", "name": "x", "type": "nsgroup:stubmember"}
    obj = Allnsgroup.model_validate(raw)
    assert obj.type_ == "nsgroup:stubmember"
    dumped = obj.model_dump(by_alias=True, exclude_none=True)
    assert dumped["type"] == "nsgroup:stubmember"
    assert "type_" not in dumped


async def test_allnsgroup_update_strips_readonly() -> None:
    """All non-ref fields are read-only; none should appear in a PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "allnsgroup/ZG5z:x", "name": "x", "type": "nsgroup"})

    async with _client(handler) as c:
        ref = "allnsgroup/ZG5z:x"
        g = Allnsgroup(**{"_ref": ref, "name": "x", "type": "nsgroup", "comment": "note"})
        await c.dns.allnsgroup.update(ref, g)
        body = captured[0].content.decode()
        # All three payload fields are in READONLY_FIELDS - should be stripped
        assert '"name"' not in body
        assert '"comment"' not in body
        assert '"type"' not in body


async def test_allnsgroup_delete() -> None:
    """delete() returns the ref string (WAPI would 400 in reality; SDK allows it)."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("allnsgroup/ZG5z:x")

    async with _client(handler) as c:
        result = await c.dns.allnsgroup.delete("allnsgroup/ZG5z:x")
        assert result == "allnsgroup/ZG5z:x"
