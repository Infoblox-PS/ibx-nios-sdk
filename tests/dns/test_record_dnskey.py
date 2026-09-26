# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDnskeyResource - 6-scenario test suite (DNSSEC, almost all fields RO)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_dnskey import RecordDnskey
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


_REF = "record:dnskey/ZG5z:example.com/default"

_PAYLOAD = {
    "_ref": _REF,
    "name": "example.com",
    "algorithm": "RSASHA256",
    "key_tag": 12345,
    "flags": 257,
    "view": "default",
    "zone": "example.com",
}

# ---------------------------------------------------------------------------
# 1. list(view="default")
# ---------------------------------------------------------------------------


async def test_record_dnskey_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_PAYLOAD], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.dns.record_dnskey.list(view="default").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.algorithm == "RSASHA256"
        assert r.key_tag == 12345

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_dnskey_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_PAYLOAD)

    async with _client(handler) as c:
        r = await c.dns.record_dnskey.get(_REF)
        assert r.name == "example.com"
        assert r.algorithm == "RSASHA256"
        assert r.flags == 257
        assert r.view == "default"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_dnskey_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_PAYLOAD], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dns.record_dnskey.find_one(name="example.com")
        assert r is not None
        assert r.name == "example.com"
        assert r.key_tag == 12345


# ---------------------------------------------------------------------------
# 4. create - POST body correct
# ---------------------------------------------------------------------------


async def test_record_dnskey_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_PAYLOAD)

    async with _client(handler) as c:
        r = await c.dns.record_dnskey.create({"name": "example.com", "view": "default"})
        assert r.name == "example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - almost every field is RO
# ---------------------------------------------------------------------------


async def test_record_dnskey_update_strips_readonly() -> None:
    """All 15 RO fields must be absent from PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_PAYLOAD)

    async with _client(handler) as c:
        r = RecordDnskey(
            name="example.com",  # RO
            algorithm="RSASHA256",  # RO
            key_tag=12345,  # RO
            flags=257,  # RO
            view="default",  # RO
            zone="example.com",  # RO
            comment="signed zone",  # RO
            creation_time=1700000000,  # RO
            creator="STATIC",  # RO
            dns_name="example.com.",  # RO
            last_queried=1700000001,  # RO
            public_key="AQPJ...",  # RO
            ttl=3600,  # RO
            use_ttl=True,  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.record_dnskey.update(_REF, r)
        body = captured[0].content.decode()

        # All 15 readonly fields must not appear
        for ro_field in [
            "algorithm",
            "comment",
            "creation_time",
            "creator",
            "dns_name",
            "flags",
            "key_tag",
            "last_queried",
            "name",
            "public_key",
            "ttl",
            "use_ttl",
            "uuid",
            "view",
            "zone",
        ]:
            assert f'"{ro_field}"' not in body, f"{ro_field} is readonly - must be stripped"


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_dnskey_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dns.record_dnskey.delete(_REF)
        assert result == _REF
