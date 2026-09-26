# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MultiregionsResource - list, get, find_one, update_strips_readonly (GET+PUT only, no POST/DELETE)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.cloud.models.multiregions import Multiregions
from tests.conftest import json_response

WAPI_TYPE = "multiregions"
REF = f"{WAPI_TYPE}/ZG5z:mr1"


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


async def test_multiregions_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"result": [{"_ref": REF, "cloud_platform": "AWS"}], "next_page_id": ""}
        )

    async with _client(handler) as c:
        records = await c.cloud.multiregions.list().all()
        assert len(records) == 1
        assert records[0].cloud_platform == "AWS"
        assert captured[0].url.params["_paging"] == "1"


async def test_multiregions_get() -> None:
    async with _client(_session_handler({"_ref": REF, "cloud_platform": "AZURE"})) as c:
        r = await c.cloud.multiregions.get(REF)
        assert r.cloud_platform == "AZURE"
        assert r.ref == REF


async def test_multiregions_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "cloud_platform": "GCP"}], "next_page_id": ""})
    ) as c:
        r = await c.cloud.multiregions.find_one(cloud_platform="GCP")
        assert r is not None
        assert r.cloud_platform == "GCP"


async def test_multiregions_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "cloud_platform": "AWS"})

    async with _client(handler) as c:
        obj = Multiregions(**{"_ref": REF, "cloud_platform": "AWS", "uuid": "ro-uuid"})
        await c.cloud.multiregions.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"AWS"' in body


async def test_multiregions_model_fields() -> None:
    """Verify that model fields are properly set.

    regions and govcloud_regions are comma-separated strings as returned by the
    WAPI (schema type ``string``, not a list).
    """
    obj = Multiregions(
        **{
            "_ref": REF,
            "cloud_platform": "AWS",
            "govcloud_regions": "us-gov-east-1",
            "regions": "us-east-1,us-west-2",
        }
    )
    assert obj.cloud_platform == "AWS"
    assert obj.govcloud_regions == "us-gov-east-1"
    assert obj.regions == "us-east-1,us-west-2"
    # callers can split on comma to get a list
    assert obj.regions.split(",") == ["us-east-1", "us-west-2"]


async def test_multiregions_wapi_type() -> None:
    """Verify wapi_type is correct."""
    from ibx_nios_sdk.cloud._multiregions import MultiregionsResource

    assert MultiregionsResource._wapi_type == "multiregions"
