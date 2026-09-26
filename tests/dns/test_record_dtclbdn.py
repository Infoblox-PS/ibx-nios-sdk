# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDtclbdnResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_dtclbdn import RecordDtclbdn
from tests.conftest import json_response

WAPI_TYPE = "record:dtclbdn"
REF = f"{WAPI_TYPE}/ZG5z:lbdn.example.com/default"


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


async def test_record_dtclbdn_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.dns.record_dtclbdn._wapi_type == WAPI_TYPE


async def test_record_dtclbdn_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "lbdn.example.com",
                        "view": "default",
                        "zone": "example.com",
                        "pattern": "*.example.com",
                        "comment": "dtc lbdn",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        records = await c.dns.record_dtclbdn.list().all()
        assert len(records) == 1
        assert records[0].name == "lbdn.example.com"
        assert records[0].pattern == "*.example.com"


async def test_record_dtclbdn_get_by_ref() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "lbdn.example.com",
                "view": "default",
                "zone": "example.com",
                "pattern": "*.example.com",
                "comment": "",
                "disable": False,
            }
        )
    ) as c:
        r = await c.dns.record_dtclbdn.get(REF)
        assert r.ref == REF
        assert r.name == "lbdn.example.com"
        assert r.zone == "example.com"


async def test_record_dtclbdn_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "lbdn.example.com",
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.dns.record_dtclbdn.find_one(name="lbdn.example.com")
        assert r is not None
        assert r.name == "lbdn.example.com"


async def test_record_dtclbdn_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "lbdn.example.com"})

    async with _client(handler) as c:
        r = await c.dns.record_dtclbdn.create({"name": "lbdn.example.com"})
        assert r.ref == REF
        req = captured[0]
        assert req.method == "POST"
        assert '"lbdn.example.com"' in req.content.decode()


async def test_record_dtclbdn_update_strips_readonly() -> None:
    """RecordDtclbdn has every field readonly - update body only has extattrs (writable)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "lbdn.example.com"})

    async with _client(handler) as c:
        obj = RecordDtclbdn(
            name="lbdn.example.com",
            comment="ro",
            disable=False,
            last_queried=1,
            lbdn="dtc:lbdn/x",
            pattern="*",
            uuid="u",
            view="default",
            zone="example.com",
            extattrs={},
        )
        await c.dns.record_dtclbdn.update(REF, obj)
        body = captured[0].content.decode()
        for ro in (
            "comment",
            "disable",
            "last_queried",
            "lbdn",
            "name",
            "pattern",
            "uuid",
            "view",
            "zone",
        ):
            assert f'"{ro}"' not in body, f"{ro} is readonly - must be stripped"


async def test_record_dtclbdn_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.dns.record_dtclbdn.delete(REF) == REF
