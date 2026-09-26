# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscribersiteResource - CRUD, find_one, list, readonly+create-only strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.parentalcontrol_subscribersite import (
    ParentalcontrolSubscribersite,
)
from tests.conftest import json_response

WAPI_TYPE = "parentalcontrol:subscribersite"
REF = f"{WAPI_TYPE}/ZG5z:site1"


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


async def test_parentalcontrol_subscribersite_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.security.parentalcontrol_subscribersite._wapi_type == WAPI_TYPE


async def test_parentalcontrol_subscribersite_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "site1",
                        "blocking_ipv4_vip1": "10.0.0.1",
                        "blocking_ipv4_vip2": "10.0.0.2",
                        "maximum_subscribers": 1000,
                        "comment": "test site",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        sites = await c.security.parentalcontrol_subscribersite.list().all()
        assert len(sites) == 1
        assert sites[0].name == "site1"
        assert sites[0].maximum_subscribers == 1000


async def test_parentalcontrol_subscribersite_get_by_ref() -> None:
    async with _client(_session_handler({"_ref": REF, "name": "site1"})) as c:
        r = await c.security.parentalcontrol_subscribersite.get(REF)
        assert r.ref == REF
        assert r.name == "site1"


async def test_parentalcontrol_subscribersite_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "site1"}], "next_page_id": ""})
    ) as c:
        r = await c.security.parentalcontrol_subscribersite.find_one(name="site1")
        assert r is not None
        assert r.name == "site1"


async def test_parentalcontrol_subscribersite_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "site1"})

    async with _client(handler) as c:
        r = await c.security.parentalcontrol_subscribersite.create({"name": "site1"})
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"site1"' in body


async def test_parentalcontrol_subscribersite_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "site1"})

    async with _client(handler) as c:
        obj = ParentalcontrolSubscribersite(
            name="site1",  # create-only - stripped on update
            comment="updated",
            maximum_subscribers=2000,
            api_port=443,  # RO
            uuid="ro-uuid",  # RO
        )
        await c.security.parentalcontrol_subscribersite.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"api_port"' not in body
        assert '"name"' not in body, "name is create-only - stripped on update"
        assert '"comment":"updated"' in body
        assert '"maximum_subscribers":2000' in body


async def test_parentalcontrol_subscribersite_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.security.parentalcontrol_subscribersite.delete(REF) == REF
