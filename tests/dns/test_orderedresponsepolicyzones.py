# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""OrderedresponsepolicyzonesResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.orderedresponsepolicyzones import Orderedresponsepolicyzones
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
# 1. list with view filter
# ---------------------------------------------------------------------------


async def test_orderedresponsepolicyzones_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "orderedresponsepolicyzones/ZG5z:default",
                        "view": "default",
                        "rp_zones": [
                            "zone_rp/ZG5z:rpz1.example.com/default",
                            "zone_rp/ZG5z:rpz2.example.com/default",
                        ],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        results = await c.dns.orderedresponsepolicyzones.list(view="default").all()
        assert len(results) == 1
        r = results[0]
        assert r.view == "default"
        assert r.rp_zones is not None
        assert len(r.rp_zones) == 2

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "view" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref - returns populated model
# ---------------------------------------------------------------------------


async def test_orderedresponsepolicyzones_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "orderedresponsepolicyzones/ZG5z:default",
                "view": "default",
                "rp_zones": [
                    "zone_rp/ZG5z:rpz1.example.com/default",
                    "zone_rp/ZG5z:rpz2.example.com/default",
                    "zone_rp/ZG5z:rpz3.example.com/default",
                ],
            }
        )

    async with _client(handler) as c:
        ref = "orderedresponsepolicyzones/ZG5z:default"
        r = await c.dns.orderedresponsepolicyzones.get(ref)
        assert r.view == "default"
        assert r.rp_zones is not None
        assert len(r.rp_zones) == 3
        assert r.rp_zones[0] == "zone_rp/ZG5z:rpz1.example.com/default"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_orderedresponsepolicyzones_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "orderedresponsepolicyzones/ZG5z:default",
                        "view": "default",
                        "rp_zones": [],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.orderedresponsepolicyzones.find_one(view="default")
        assert r is not None
        assert r.view == "default"


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_orderedresponsepolicyzones_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "orderedresponsepolicyzones/ZG5z:custom",
                "view": "custom",
                "rp_zones": ["zone_rp/ZG5z:rpz1.example.com/custom"],
            }
        )

    async with _client(handler) as c:
        r = await c.dns.orderedresponsepolicyzones.create(
            {
                "view": "custom",
                "rp_zones": ["zone_rp/ZG5z:rpz1.example.com/custom"],
            }
        )
        assert r.view == "custom"
        body = captured[0].content.decode()
        assert '"view":"custom"' in body
        assert '"rp_zones"' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_orderedresponsepolicyzones_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "orderedresponsepolicyzones/ZG5z:default",
                "view": "default",
                "rp_zones": ["zone_rp/ZG5z:rpz1.example.com/default"],
            }
        )

    async with _client(handler) as c:
        ref = "orderedresponsepolicyzones/ZG5z:default"
        r = Orderedresponsepolicyzones(
            view="default",
            rp_zones=["zone_rp/ZG5z:rpz1.example.com/default"],
            uuid="some-uuid",  # RO
        )
        await c.dns.orderedresponsepolicyzones.update(ref, r)
        body = captured[0].content.decode()
        # Readonly field must not appear
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        # Writable fields must be present
        assert '"view":"default"' in body
        assert '"rp_zones"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_orderedresponsepolicyzones_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("orderedresponsepolicyzones/ZG5z:default")

    async with _client(handler) as c:
        result = await c.dns.orderedresponsepolicyzones.delete(
            "orderedresponsepolicyzones/ZG5z:default"
        )
        assert result == "orderedresponsepolicyzones/ZG5z:default"
