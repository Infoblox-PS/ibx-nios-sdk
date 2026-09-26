# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyRuleResource - list, get, find_one, update_strips_readonly."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_topology_rule import DtcTopologyRule
from tests.conftest import json_response

WAPI_TYPE = "dtc:topology:rule"
REF = f"{WAPI_TYPE}/ZG5z:rule1"


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


def _session_handler(body: Any) -> Any:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(body)

    return handler


async def test_dtc_topology_rule_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [{"_ref": REF, "dest_type": "POOL"}], "next_page_id": ""})

    async with _client(handler) as c:
        records = await c.dtc.topology_rule.list().all()
        assert len(records) == 1
        assert records[0].dest_type == "POOL"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_topology_rule_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "dest_type": "POOL", "return_type": "REGULAR"})
    ) as c:
        r = await c.dtc.topology_rule.get(REF)
        assert r.dest_type == "POOL"


async def test_dtc_topology_rule_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "dest_type": "POOL"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.topology_rule.find_one()
        assert r is not None
        assert r.dest_type == "POOL"


async def test_dtc_topology_rule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "dest_type": "POOL"})

    async with _client(handler) as c:
        obj = DtcTopologyRule(
            **{
                "_ref": REF,
                "dest_type": "POOL",
                "topology": "ro-topo",
                "uuid": "ro-uuid",
                "valid": True,
            }
        )
        await c.dtc.topology_rule.update(REF, obj)
        body = captured[0].content.decode()
        assert '"topology"' not in body
        assert '"uuid"' not in body
        assert '"valid"' not in body
        assert '"POOL"' in body


async def test_dtc_topology_rule_model_sources() -> None:
    obj = DtcTopologyRule(**{"_ref": REF, "sources": [{"type": "SUBNET", "value": "10.0.0.0/8"}]})
    assert obj.sources is not None
    assert obj.sources[0]["type"] == "SUBNET"


async def test_dtc_topology_rule_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc_topology_rule import DtcTopologyRuleResource

    assert DtcTopologyRuleResource._wapi_type == "dtc:topology:rule"
