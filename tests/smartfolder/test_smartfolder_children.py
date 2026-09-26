# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderChildrenResource - list, get, find_one (GET only, no POST/PUT/DELETE)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "smartfolder:children"
REF = f"{WAPI_TYPE}/ZG5z:child1"


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


async def test_smartfolder_children_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "resource": "network/ZG5z", "value_type": "STRING"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.smartfolder.children.list().all()
        assert len(records) == 1
        assert records[0].resource == "network/ZG5z"
        assert records[0].value_type == "STRING"
        assert captured[0].url.params["_paging"] == "1"


async def test_smartfolder_children_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "resource": "network/ZG5z", "value_type": "STRING"})
    ) as c:
        r = await c.smartfolder.children.get(REF)
        assert r.resource == "network/ZG5z"
        assert r.ref == REF


async def test_smartfolder_children_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "resource": "network/ZG5z"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.smartfolder.children.find_one()
        assert r is not None
        assert r.resource == "network/ZG5z"


async def test_smartfolder_children_model_fields() -> None:
    """Verify model fields are correct."""
    from ibx_nios_sdk.smartfolder.models.smartfolder_children import SmartfolderChildren

    obj = SmartfolderChildren(
        **{
            "_ref": REF,
            "resource": "network/ZG5z",
            "value_type": "INTEGER",
            "value": {"val": 42},
        }
    )
    assert obj.ref == REF
    assert obj.resource == "network/ZG5z"
    assert obj.value_type == "INTEGER"
    assert obj.value == {"val": 42}


async def test_smartfolder_children_wapi_type() -> None:
    """Verify wapi_type is correct."""
    from ibx_nios_sdk.smartfolder._smartfolder_children import SmartfolderChildrenResource

    assert SmartfolderChildrenResource._wapi_type == "smartfolder:children"


async def test_smartfolder_children_readonly_fields() -> None:
    """Readonly fields should include resource and value_type."""
    from ibx_nios_sdk.smartfolder.models.smartfolder_children import READONLY_FIELDS

    assert "resource" in READONLY_FIELDS
    assert "value_type" in READONLY_FIELDS
