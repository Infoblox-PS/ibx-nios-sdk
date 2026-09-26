# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmAllgroupsResource - list, get, find_one, create, update_strips_readonly, delete."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.hsm_allgroups import HsmAllgroups
from tests.conftest import json_response

WAPI_TYPE = "hsm:allgroups"
REF = f"{WAPI_TYPE}/ZG5z:allgroups"


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


async def test_hsm_allgroups_list() -> None:
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
                        "groups": ["hsm:thaleslunagroup/ZG5z:luna1"],
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.security.hsm_allgroups.list().all()
        assert len(records) == 1
        assert records[0].groups == ["hsm:thaleslunagroup/ZG5z:luna1"]
        assert captured[0].url.params["_paging"] == "1"


async def test_hsm_allgroups_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "groups": ["hsm:thaleslunagroup/ZG5z:luna1"]})
    ) as c:
        r = await c.security.hsm_allgroups.get(REF)
        assert r.groups == ["hsm:thaleslunagroup/ZG5z:luna1"]


async def test_hsm_allgroups_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "groups": ["hsm:thaleslunagroup/ZG5z:luna1"]}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.security.hsm_allgroups.find_one()
        assert r is not None
        assert r.groups is not None


async def test_hsm_allgroups_create() -> None:
    """hsm:allgroups create - WapiResource.create available (aggregate object)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "groups": []})

    async with _client(handler) as c:
        r = await c.security.hsm_allgroups.create({})
        assert r.ref == REF
        req = captured[0]
        assert req.method == "POST"


async def test_hsm_allgroups_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "groups": ["hsm:thaleslunagroup/ZG5z:luna1"]})

    async with _client(handler) as c:
        obj = HsmAllgroups(**{"_ref": REF, "groups": ["hsm:thaleslunagroup/ZG5z:luna1"]})
        await c.security.hsm_allgroups.update(REF, obj)
        body = captured[0].content.decode()
        # No readOnly fields for HsmAllgroups
        assert '"groups"' in body


async def test_hsm_allgroups_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        result = await c.security.hsm_allgroups.delete(REF)
        assert result == REF
