# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneAuthDiscrepancyResource - list, get, find_one, readonly-strip, delete.

ZoneAuthDiscrepancy is a read-only aggregate; all non-_ref fields are readOnly
in swagger.  create/update/delete exist on the resource but WAPI will reject them.
"""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.zone_auth_discrepancy import ZoneAuthDiscrepancy
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
# 1. list
# ---------------------------------------------------------------------------


async def test_zone_auth_discrepancy_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_auth_discrepancy/ZG5z:abc123",
                        "zone": "example.com",
                        "description": "SOA serial mismatch",
                        "severity": "WARNING",
                        "timestamp": 1700000000,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        items = await c.dns.zone_auth_discrepancy.list().all()
        assert len(items) == 1
        d = items[0]
        assert d.zone == "example.com"
        assert d.description == "SOA serial mismatch"
        assert d.severity == "WARNING"
        assert d.timestamp == 1700000000

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "zone" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref
# ---------------------------------------------------------------------------


async def test_zone_auth_discrepancy_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "zone_auth_discrepancy/ZG5z:abc123",
                "zone": "example.com",
                "description": "Zone not found on secondary",
                "severity": "CRITICAL",
                "timestamp": 1700000001,
                "uuid": "abc123-uuid",
            }
        )

    async with _client(handler) as c:
        ref = "zone_auth_discrepancy/ZG5z:abc123"
        d = await c.dns.zone_auth_discrepancy.get(ref)
        assert d.zone == "example.com"
        assert d.description == "Zone not found on secondary"
        assert d.severity == "CRITICAL"
        assert d.timestamp == 1700000001
        assert d.uuid == "abc123-uuid"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_zone_auth_discrepancy_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_auth_discrepancy/ZG5z:abc123",
                        "zone": "example.com",
                        "description": "SOA serial mismatch",
                        "severity": "WARNING",
                        "timestamp": 1700000000,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        d = await c.dns.zone_auth_discrepancy.find_one(zone="example.com")
        assert d is not None
        assert d.zone == "example.com"
        assert d.severity == "WARNING"


# ---------------------------------------------------------------------------
# 4. update strips readonly fields (all non-_ref fields are readonly)
# ---------------------------------------------------------------------------


async def test_zone_auth_discrepancy_update_strips_readonly() -> None:
    """All non-ref fields are read-only; none should appear in a PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_auth_discrepancy/ZG5z:abc123",
                "zone": "example.com",
                "severity": "WARNING",
            }
        )

    async with _client(handler) as c:
        ref = "zone_auth_discrepancy/ZG5z:abc123"
        d = ZoneAuthDiscrepancy(
            **{
                "_ref": ref,
                "zone": "example.com",
                "description": "SOA serial mismatch",
                "severity": "WARNING",
                "timestamp": 1700000000,
                "uuid": "abc123-uuid",
            }
        )
        await c.dns.zone_auth_discrepancy.update(ref, d)
        body = captured[0].content.decode()
        # All payload fields are in READONLY_FIELDS - should be stripped
        assert '"zone"' not in body
        assert '"description"' not in body
        assert '"severity"' not in body
        assert '"timestamp"' not in body
        assert '"uuid"' not in body


# ---------------------------------------------------------------------------
# 5. delete returns ref (WAPI would 400 in reality; SDK allows it)
# ---------------------------------------------------------------------------


async def test_zone_auth_discrepancy_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("zone_auth_discrepancy/ZG5z:abc123")

    async with _client(handler) as c:
        result = await c.dns.zone_auth_discrepancy.delete("zone_auth_discrepancy/ZG5z:abc123")
        assert result == "zone_auth_discrepancy/ZG5z:abc123"


# ---------------------------------------------------------------------------
# 6. model validates all read-only fields correctly
# ---------------------------------------------------------------------------


async def test_zone_auth_discrepancy_model_fields() -> None:
    """All swagger fields parse correctly from a dict."""
    raw = {
        "_ref": "zone_auth_discrepancy/ZG5z:abc123",
        "zone": "test.example.com",
        "description": "NS record mismatch",
        "severity": "INFO",
        "timestamp": 1699999999,
        "uuid": "deadbeef-uuid",
    }
    d = ZoneAuthDiscrepancy.model_validate(raw)
    assert d.ref == "zone_auth_discrepancy/ZG5z:abc123"
    assert d.zone == "test.example.com"
    assert d.description == "NS record mismatch"
    assert d.severity == "INFO"
    assert d.timestamp == 1699999999
    assert d.uuid == "deadbeef-uuid"
