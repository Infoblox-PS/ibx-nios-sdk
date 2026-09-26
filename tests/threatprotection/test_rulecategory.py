# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRulecategoryResource - list, get, find_one, model_roundtrip, readonly_strip, type_check."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_rulecategory import (
    ThreatprotectionRulecategory,
)
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:rulecategory"
REF = f"{WAPI_TYPE}/ZG5z:dns-recon"
RULESET_REF = "threatprotection:ruleset/ZG5z:v1.0"


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


# 1. list
async def test_rulecategory_list() -> None:
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
                        "name": "dns-recon",
                        "ruleset": RULESET_REF,
                        "uuid": "cat-uuid-1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.rulecategory.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "dns-recon"
        assert r.ruleset == RULESET_REF
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_rulecategory_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "dns-recon",
                "ruleset": RULESET_REF,
                "uuid": "cat-uuid-1",
                "is_factory_reset_enabled": True,
            }
        )
    ) as c:
        r = await c.threatprotection.rulecategory.get(REF)
        assert r.name == "dns-recon"
        assert r.is_factory_reset_enabled is True


# 3. find_one
async def test_rulecategory_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "dns-recon",
                        "ruleset": RULESET_REF,
                        "uuid": "cat-uuid-1",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.rulecategory.find_one(name="dns-recon")
        assert r is not None
        assert r.name == "dns-recon"


# 4. model roundtrip validates all readonly fields
async def test_rulecategory_model_roundtrip() -> None:
    data = {
        "_ref": REF,
        "name": "dns-recon",
        "ruleset": RULESET_REF,
        "uuid": "cat-uuid-1",
        "is_factory_reset_enabled": False,
    }
    obj = ThreatprotectionRulecategory.model_validate(data)
    assert obj.name == "dns-recon"
    assert obj.uuid == "cat-uuid-1"
    assert obj.is_factory_reset_enabled is False


# 5. update strips all readonly fields
async def test_rulecategory_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "dns-recon",
                "ruleset": RULESET_REF,
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionRulecategory.model_validate(
            {"name": "dns-recon", "ruleset": RULESET_REF, "uuid": "cat-uuid-1"}
        )
        await c.threatprotection.rulecategory.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"ruleset"' not in body, "ruleset is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"


# 6. resource is accessible as cached property on service
async def test_rulecategory_resource_type() -> None:
    from ibx_nios_sdk.threatprotection._rulecategory import ThreatprotectionRulecategoryResource

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({})

    c = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )
    assert isinstance(c.threatprotection.rulecategory, ThreatprotectionRulecategoryResource)
