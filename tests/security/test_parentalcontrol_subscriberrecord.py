# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscriberrecordResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.parentalcontrol_subscriberrecord import (
    ParentalcontrolSubscriberrecord,
)
from tests.conftest import json_response

WAPI_TYPE = "parentalcontrol:subscriberrecord"
REF = f"{WAPI_TYPE}/ZG5z:rec1"


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


async def test_parentalcontrol_subscriberrecord_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.security.parentalcontrol_subscriberrecord._wapi_type == WAPI_TYPE


async def test_parentalcontrol_subscriberrecord_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "subscriber_id": "sub1",
                        "ip_addr": "10.0.0.1",
                        "site": "site1",
                        "parental_control_policy": "policy1",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        recs = await c.security.parentalcontrol_subscriberrecord.list().all()
        assert len(recs) == 1
        assert recs[0].subscriber_id == "sub1"
        assert recs[0].ip_addr == "10.0.0.1"


async def test_parentalcontrol_subscriberrecord_get_by_ref() -> None:
    async with _client(
        _session_handler({"_ref": REF, "subscriber_id": "sub1", "ip_addr": "10.0.0.1"})
    ) as c:
        r = await c.security.parentalcontrol_subscriberrecord.get(REF)
        assert r.ref == REF
        assert r.ip_addr == "10.0.0.1"


async def test_parentalcontrol_subscriberrecord_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "subscriber_id": "sub1"}], "next_page_id": ""})
    ) as c:
        r = await c.security.parentalcontrol_subscriberrecord.find_one(subscriber_id="sub1")
        assert r is not None
        assert r.subscriber_id == "sub1"


async def test_parentalcontrol_subscriberrecord_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "subscriber_id": "sub1"})

    async with _client(handler) as c:
        r = await c.security.parentalcontrol_subscriberrecord.create(
            {"subscriber_id": "sub1", "ip_addr": "10.0.0.1"}
        )
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"sub1"' in body


async def test_parentalcontrol_subscriberrecord_update_strips_readonly() -> None:
    """READONLY_FIELDS is empty - all fields are writable."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "subscriber_id": "sub1"})

    async with _client(handler) as c:
        obj = ParentalcontrolSubscriberrecord(
            subscriber_id="sub1",
            ip_addr="10.0.0.2",
            site="site1",
        )
        await c.security.parentalcontrol_subscriberrecord.update(REF, obj)
        body = captured[0].content.decode()
        assert '"ip_addr":"10.0.0.2"' in body
        assert '"subscriber_id":"sub1"' in body


async def test_parentalcontrol_subscriberrecord_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.security.parentalcontrol_subscriberrecord.delete(REF) == REF
