# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RirOrganizationResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.rir_organization import RirOrganization
from tests.conftest import json_response

WAPI_TYPE = "rir:organization"
REF = f"{WAPI_TYPE}/ZG5z:ORG-EX1-RIPE"


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


async def test_rir_organization_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.ipam.rir_organization._wapi_type == WAPI_TYPE


async def test_rir_organization_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "ExampleOrg",
                        "id": "ORG-EX1-RIPE",
                        "rir": "rir/RIPE",
                        "maintainer": "ExampleMaint",
                        "sender_email": "hostmaster@example.com",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        orgs = await c.ipam.rir_organization.list().all()
        assert len(orgs) == 1
        assert orgs[0].id == "ORG-EX1-RIPE"
        assert orgs[0].maintainer == "ExampleMaint"


async def test_rir_organization_get_by_ref() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "ExampleOrg", "id": "ORG-EX1-RIPE"})
    ) as c:
        r = await c.ipam.rir_organization.get(REF)
        assert r.ref == REF
        assert r.name == "ExampleOrg"


async def test_rir_organization_find_one() -> None:
    async with _client(
        _session_handler(
            {
                "result": [{"_ref": REF, "name": "ExampleOrg", "id": "ORG-EX1-RIPE"}],
                "next_page_id": "",
            }
        )
    ) as c:
        r = await c.ipam.rir_organization.find_one(name="ExampleOrg")
        assert r is not None
        assert r.id == "ORG-EX1-RIPE"


async def test_rir_organization_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "ExampleOrg"})

    async with _client(handler) as c:
        r = await c.ipam.rir_organization.create(
            {"name": "ExampleOrg", "id": "ORG-EX1-RIPE", "rir": "rir/RIPE"}
        )
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"ExampleOrg"' in body
        assert '"ORG-EX1-RIPE"' in body


async def test_rir_organization_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "ExampleOrg"})

    async with _client(handler) as c:
        obj = RirOrganization(
            name="ExampleOrg",
            id="ORG-EX1-RIPE",
            maintainer="ExampleMaint",
            uuid="ro-uuid",
        )
        await c.ipam.rir_organization.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"maintainer":"ExampleMaint"' in body


async def test_rir_organization_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.ipam.rir_organization.delete(REF) == REF
