# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyLabelResource - list, get, find_one (read-only)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_topology_label import DtcTopologyLabel
from tests.conftest import json_response

WAPI_TYPE = "dtc:topology:label"
REF = f"{WAPI_TYPE}/ZG5z:label1"


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


async def test_dtc_topology_label_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "field": "CONTINENT", "label": "EU"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.dtc.topology_label.list().all()
        assert len(records) == 1
        assert records[0].field == "CONTINENT"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_topology_label_get() -> None:
    async with _client(_session_handler({"_ref": REF, "field": "CONTINENT", "label": "EU"})) as c:
        r = await c.dtc.topology_label.get(REF)
        assert r.field == "CONTINENT"
        assert r.label == "EU"


async def test_dtc_topology_label_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "field": "CONTINENT"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.topology_label.find_one()
        assert r is not None
        assert r.field == "CONTINENT"


async def test_dtc_topology_label_model_fields() -> None:
    obj = DtcTopologyLabel(**{"_ref": REF, "field": "COUNTRY", "label": "US"})
    assert obj.field == "COUNTRY"
    assert obj.label == "US"
    assert obj.ref == REF


async def test_dtc_topology_label_readonly_fields() -> None:
    from ibx_nios_sdk.dtc.models.dtc_topology_label import READONLY_FIELDS

    assert "field" in READONLY_FIELDS
    assert "label" in READONLY_FIELDS


async def test_dtc_topology_label_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc_topology_label import DtcTopologyLabelResource

    assert DtcTopologyLabelResource._wapi_type == "dtc:topology:label"
