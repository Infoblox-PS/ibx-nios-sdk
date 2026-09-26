# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcCertificateResource - list, get, find_one (read-only)."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dtc.models.dtc_certificate import DtcCertificate
from tests.conftest import json_response

WAPI_TYPE = "dtc:certificate"
REF = f"{WAPI_TYPE}/ZG5z:cert1"


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


async def test_dtc_certificate_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "uuid": "abc-123", "in_use": True}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dtc.certificate.list().all()
        assert len(records) == 1
        assert records[0].uuid == "abc-123"
        assert captured[0].url.params["_paging"] == "1"


async def test_dtc_certificate_get() -> None:
    async with _client(_session_handler({"_ref": REF, "uuid": "abc-123", "in_use": False})) as c:
        r = await c.dtc.certificate.get(REF)
        assert r.uuid == "abc-123"
        assert r.in_use is False


async def test_dtc_certificate_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "uuid": "abc-123"}], "next_page_id": ""})
    ) as c:
        r = await c.dtc.certificate.find_one()
        assert r is not None
        assert r.uuid == "abc-123"


async def test_dtc_certificate_model_fields() -> None:
    obj = DtcCertificate(
        **{"_ref": REF, "uuid": "abc-123", "in_use": True, "certificate": "PEM..."}
    )
    assert obj.uuid == "abc-123"
    assert obj.in_use is True
    assert obj.certificate == "PEM..."


async def test_dtc_certificate_readonly_fields() -> None:
    from ibx_nios_sdk.dtc.models.dtc_certificate import READONLY_FIELDS

    assert "uuid" in READONLY_FIELDS
    assert "in_use" in READONLY_FIELDS
    assert "certificate" in READONLY_FIELDS


async def test_dtc_certificate_wapi_type() -> None:
    from ibx_nios_sdk.dtc._dtc_certificate import DtcCertificateResource

    assert DtcCertificateResource._wapi_type == "dtc:certificate"
