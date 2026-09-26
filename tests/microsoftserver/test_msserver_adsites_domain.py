# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverAdsitesDomainResource - list, get, find_one, readonly, model, wapi_type."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response

WAPI_TYPE = "msserver:adsites:domain"
REF = f"{WAPI_TYPE}/ZG5z:dom1"


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


async def test_msserver_adsites_domain_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [{"_ref": REF, "name": "corp.com", "netbios": "CORP"}],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.microsoftserver.adsites_domain.list().all()
        assert len(records) == 1
        assert records[0].name == "corp.com"
        assert records[0].netbios == "CORP"
        assert captured[0].url.params["_paging"] == "1"


async def test_msserver_adsites_domain_get() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "corp.com", "network_view": "default"})
    ) as c:
        r = await c.microsoftserver.adsites_domain.get(REF)
        assert r.name == "corp.com"


async def test_msserver_adsites_domain_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "corp.com"}], "next_page_id": ""})
    ) as c:
        r = await c.microsoftserver.adsites_domain.find_one(name="corp.com")
        assert r is not None
        assert r.name == "corp.com"


async def test_msserver_adsites_domain_readonly_check() -> None:
    from ibx_nios_sdk.microsoftserver._msserver_adsites_domain import (
        MsserverAdsitesDomainResource,
    )

    assert "name" in MsserverAdsitesDomainResource._readonly_fields
    assert "netbios" in MsserverAdsitesDomainResource._readonly_fields
    assert "uuid" in MsserverAdsitesDomainResource._readonly_fields


async def test_msserver_adsites_domain_model_fields() -> None:
    from ibx_nios_sdk.microsoftserver.models.msserver_adsites_domain import MsserverAdsitesDomain

    obj = MsserverAdsitesDomain(
        **{"_ref": REF, "name": "corp.com", "netbios": "CORP", "read_only": False}
    )
    assert obj.name == "corp.com"
    assert obj.read_only is False


async def test_msserver_adsites_domain_wapi_type() -> None:
    from ibx_nios_sdk.microsoftserver._msserver_adsites_domain import (
        MsserverAdsitesDomainResource,
    )

    assert MsserverAdsitesDomainResource._wapi_type == "msserver:adsites:domain"
