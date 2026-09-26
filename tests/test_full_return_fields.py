# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Regression: ``list()`` with the object's FULL readable field set must validate.

The default ``_return_fields`` set is tiny (usually ``name``/``comment``), so a
test that lists with defaults never exercises the fields whose declared type
disagrees with the wire. These tests request every readable field the WAPI
schema defines, serve a wire row shaped exactly as the schema says (lists as
lists, structs as objects, refs as strings), and require the typed model to
accept it. Real rows captured from NIOS 9.1 for the four objects originally
reported broken are checked as well.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response
from tests.wapi_schema import (
    ResourceInfo,
    iter_resources,
    load_snapshot,
    readable_field_names,
    synthesize_row,
)

RESOURCES = [r for r in iter_resources() if r.wapi_type in load_snapshot()["objects"]]
CAPTURED = Path(__file__).parent / "fixtures" / "wire_rows_nios_9_1.json"


def _client(rows: list[dict[str, Any]], captured: list[httpx.Request]) -> NiosClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": rows, "next_page_id": ""})

    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # A handful of object types (dtc, discovery, ...) restrict read, so a real
        # grid never serves these rows for them. This suite is about model parsing,
        # not the restriction gate - tests/test_object_restrictions.py covers that.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


@pytest.mark.parametrize("res", RESOURCES, ids=lambda r: r.wapi_type)
async def test_list_with_full_schema_return_fields(res: ResourceInfo) -> None:
    fields = readable_field_names(res.wapi_type)
    row = synthesize_row(res.wapi_type)
    captured: list[httpx.Request] = []
    async with _client([row], captured) as c:
        resource = res.resource(c._http)
        items = await resource.list(return_fields=fields).all()

    assert len(items) == 1
    requested = set(captured[0].url.params["_return_fields"].split(","))
    assert requested >= set(fields), "list() did not request every readable field"
    dumped = items[0].model_dump(by_alias=True)
    for name in fields:
        assert name in dumped, f"{name} was requested but did not populate the model"


def _captured_rows() -> list[tuple[str, dict[str, Any]]]:
    data = json.loads(CAPTURED.read_text())
    return [(t, row) for t, rows in data["rows"].items() for row in rows]


@pytest.mark.parametrize(
    "wapi_type,row", _captured_rows(), ids=lambda v: v if isinstance(v, str) else ""
)
async def test_list_accepts_captured_nios_rows(wapi_type: str, row: dict[str, Any]) -> None:
    res = next(r for r in RESOURCES if r.wapi_type == wapi_type)
    captured: list[httpx.Request] = []
    async with _client([row], captured) as c:
        items = await res.resource(c._http).list(return_fields=list(row)).all()
    assert items[0].model_dump(by_alias=True, exclude_none=True)["_ref"] == row["_ref"]
