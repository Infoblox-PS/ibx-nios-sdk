# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRuletemplateResource - list, get, find_one, model_roundtrip, readonly_strip, type_check."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.threatprotection.models.threatprotection_ruletemplate import (
    ThreatprotectionRuletemplate,
)
from tests.conftest import json_response

WAPI_TYPE = "threatprotection:ruletemplate"
REF = f"{WAPI_TYPE}/ZG5z:tmpl1"
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
async def test_ruletemplate_list() -> None:
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
                        "name": "DNS Recon Template",
                        "category": "dns-recon",
                        "ruleset": RULESET_REF,
                        "description": "Detects DNS recon",
                        "sid": 9000001,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.threatprotection.ruletemplate.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "DNS Recon Template"
        assert r.category == "dns-recon"
        params = captured[0].url.params
        assert params["_paging"] == "1"


# 2. get by ref
async def test_ruletemplate_get() -> None:
    async with _client(
        _session_handler(
            {
                "_ref": REF,
                "name": "DNS Recon Template",
                "category": "dns-recon",
                "ruleset": RULESET_REF,
                "description": "Detects DNS recon",
                "sid": 9000001,
                "uuid": "tmpl-uuid",
                "allowed_actions": ["PASS", "DROP"],
            }
        )
    ) as c:
        r = await c.threatprotection.ruletemplate.get(REF)
        assert r.name == "DNS Recon Template"
        assert r.sid == 9000001
        assert r.allowed_actions == ["PASS", "DROP"]


# 3. find_one
async def test_ruletemplate_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "DNS Recon Template",
                        "category": "dns-recon",
                        "ruleset": RULESET_REF,
                        "description": "Detects DNS recon",
                        "sid": 9000001,
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.threatprotection.ruletemplate.find_one(name="DNS Recon Template")
        assert r is not None
        assert r.description == "Detects DNS recon"


# 4. model roundtrip validates all fields including nested default_config
async def test_ruletemplate_model_roundtrip() -> None:
    data = {
        "_ref": REF,
        "name": "DNS Recon Template",
        "category": "dns-recon",
        "ruleset": RULESET_REF,
        "description": "Detects DNS recon",
        "sid": 9000001,
        "uuid": "tmpl-uuid",
        "allowed_actions": ["PASS", "DROP"],
        "default_config": {"action": "PASS", "log_severity": "INFO", "params": []},
    }
    obj = ThreatprotectionRuletemplate.model_validate(data)
    assert obj.name == "DNS Recon Template"
    assert obj.sid == 9000001
    assert obj.default_config is not None
    assert obj.default_config["action"] == "PASS"


# 5. update strips all readonly fields
async def test_ruletemplate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": REF,
                "name": "DNS Recon Template",
                "category": "dns-recon",
            }
        )

    async with _client(handler) as c:
        obj = ThreatprotectionRuletemplate.model_validate(
            {
                "name": "DNS Recon Template",
                "category": "dns-recon",
                "ruleset": RULESET_REF,
                "description": "some desc",
                "sid": 9000001,
                "uuid": "tmpl-uuid",
                "allowed_actions": ["PASS"],
            }
        )
        await c.threatprotection.ruletemplate.update(REF, obj)
        body = captured[0].content.decode()
        assert '"name"' not in body, "name is readonly - must be stripped"
        assert '"category"' not in body, "category is readonly - must be stripped"
        assert '"sid"' not in body, "sid is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"allowed_actions"' not in body, "allowed_actions is readonly - must be stripped"


# 6. resource is accessible as cached property on service
async def test_ruletemplate_resource_type() -> None:
    from ibx_nios_sdk.threatprotection._ruletemplate import ThreatprotectionRuletemplateResource

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
    assert isinstance(c.threatprotection.ruletemplate, ThreatprotectionRuletemplateResource)
