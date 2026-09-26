# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscriberResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.parentalcontrol_subscriber import ParentalcontrolSubscriber
from tests.conftest import json_response

WAPI_TYPE = "parentalcontrol:subscriber"
REF = f"{WAPI_TYPE}/ZG5z:sub1"


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


async def test_parentalcontrol_subscriber_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.security.parentalcontrol_subscriber._wapi_type == WAPI_TYPE


async def test_parentalcontrol_subscriber_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "subscriber_id": "User-Name",
                        "enable_parental_control": True,
                        "pc_zone_name": "pc.example.com",
                        "category_url": "https://cat.example.com",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        subs = await c.security.parentalcontrol_subscriber.list().all()
        assert len(subs) == 1
        assert subs[0].subscriber_id == "User-Name"
        assert subs[0].enable_parental_control is True


async def test_parentalcontrol_subscriber_get_by_ref() -> None:
    async with _client(_session_handler({"_ref": REF, "subscriber_id": "User-Name"})) as c:
        r = await c.security.parentalcontrol_subscriber.get(REF)
        assert r.ref == REF
        assert r.subscriber_id == "User-Name"


async def test_parentalcontrol_subscriber_find_one() -> None:
    async with _client(
        _session_handler(
            {"result": [{"_ref": REF, "subscriber_id": "User-Name"}], "next_page_id": ""}
        )
    ) as c:
        r = await c.security.parentalcontrol_subscriber.find_one(subscriber_id="User-Name")
        assert r is not None
        assert r.subscriber_id == "User-Name"


async def test_parentalcontrol_subscriber_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "subscriber_id": "User-Name"})

    async with _client(handler) as c:
        r = await c.security.parentalcontrol_subscriber.create(
            {"subscriber_id": "User-Name", "pc_zone_name": "pc.example.com"}
        )
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"User-Name"' in body


async def test_parentalcontrol_subscriber_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "subscriber_id": "User-Name"})

    async with _client(handler) as c:
        obj = ParentalcontrolSubscriber(
            subscriber_id="User-Name",
            pc_zone_name="pc.example.com",
            uuid="ro-uuid",
            zvelo_update_failure_in_days=5,
        )
        await c.security.parentalcontrol_subscriber.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"zvelo_update_failure_in_days"' not in body
        assert '"pc_zone_name":"pc.example.com"' in body


async def test_parentalcontrol_subscriber_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.security.parentalcontrol_subscriber.delete(REF) == REF
