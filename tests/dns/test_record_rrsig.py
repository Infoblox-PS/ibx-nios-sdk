# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRrsigResource - 6-scenario test suite (DNSSEC RRSIG record, almost all fields RO)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_rrsig import RecordRrsig
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


_REF = "record:rrsig/ZG5z:example.com/default"

_PAYLOAD = {
    "_ref": _REF,
    "name": "example.com",
    "algorithm": "RSASHA256",
    "signer_name": "example.com",
    "type_covered": "A",
    "view": "default",
    "zone": "example.com",
}

# ---------------------------------------------------------------------------
# 1. list(zone="example.com")
# ---------------------------------------------------------------------------


async def test_record_rrsig_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_PAYLOAD], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.dns.record_rrsig.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.algorithm == "RSASHA256"
        assert r.signer_name == "example.com"
        assert r.type_covered == "A"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["zone"] == "example.com"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_rrsig_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_PAYLOAD)

    async with _client(handler) as c:
        r = await c.dns.record_rrsig.get(_REF)
        assert r.name == "example.com"
        assert r.algorithm == "RSASHA256"
        assert r.signer_name == "example.com"
        assert r.view == "default"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_rrsig_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_PAYLOAD], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.dns.record_rrsig.find_one(name="example.com")
        assert r is not None
        assert r.name == "example.com"
        assert r.type_covered == "A"


# ---------------------------------------------------------------------------
# 4. create - POST body correct
# ---------------------------------------------------------------------------


async def test_record_rrsig_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_PAYLOAD)

    async with _client(handler) as c:
        r = await c.dns.record_rrsig.create({"name": "example.com", "view": "default"})
        assert r.name == "example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly - 20 RO fields
# ---------------------------------------------------------------------------


async def test_record_rrsig_update_strips_readonly() -> None:
    """All 20 RO fields must be absent from PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_PAYLOAD)

    async with _client(handler) as c:
        r = RecordRrsig(
            algorithm="RSASHA256",  # RO
            creation_time=1700000000,  # RO
            creator="STATIC",  # RO
            dns_name="example.com.",  # RO
            dns_signer_name="example.com.",  # RO
            expiration_time=1700100000,  # RO
            inception_time=1699900000,  # RO
            key_tag=12345,  # RO
            labels=2,  # RO
            last_queried=1700000001,  # RO
            name="example.com",  # RO
            original_ttl=3600,  # RO
            signature="AABBCC==",  # RO
            signer_name="example.com",  # RO
            ttl=3600,  # RO
            type_covered="A",  # RO
            use_ttl=True,  # RO
            uuid="abc-123",  # RO
            view="default",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_rrsig.update(_REF, r)
        body = captured[0].content.decode()

        for ro_field in [
            "algorithm",
            "creation_time",
            "creator",
            "dns_name",
            "dns_signer_name",
            "expiration_time",
            "inception_time",
            "key_tag",
            "labels",
            "last_queried",
            "name",
            "original_ttl",
            "signature",
            "signer_name",
            "ttl",
            "type_covered",
            "use_ttl",
            "uuid",
            "view",
            "zone",
        ]:
            assert f'"{ro_field}"' not in body, f"{ro_field} is readonly - must be stripped"


# ---------------------------------------------------------------------------
# 6. delete(ref)
# ---------------------------------------------------------------------------


async def test_record_rrsig_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_REF)

    async with _client(handler) as c:
        result = await c.dns.record_rrsig.delete(_REF)
        assert result == _REF
