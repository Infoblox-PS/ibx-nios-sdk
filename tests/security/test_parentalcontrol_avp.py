# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolAvpResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.security.models.parentalcontrol_avp import ParentalcontrolAvp
from tests.conftest import json_response

WAPI_TYPE = "parentalcontrol:avp"
REF = f"{WAPI_TYPE}/ZG5z:avp1"


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


async def test_parentalcontrol_avp_wapi_type() -> None:
    async with _client(_session_handler({})) as c:
        assert c.security.parentalcontrol_avp._wapi_type == WAPI_TYPE


async def test_parentalcontrol_avp_list() -> None:
    async with _client(
        _session_handler(
            {
                "result": [
                    {
                        "_ref": REF,
                        "name": "avp1",
                        "type": 1,
                        "value_type": "STRING",
                        "vendor_id": 9,
                        "vendor_type": 1,
                        "comment": "test",
                    }
                ],
                "next_page_id": "",
            }
        )
    ) as c:
        avps = await c.security.parentalcontrol_avp.list().all()
        assert len(avps) == 1
        assert avps[0].name == "avp1"
        assert avps[0].value_type == "STRING"
        assert avps[0].vendor_id == 9


async def test_parentalcontrol_avp_get_by_ref() -> None:
    async with _client(
        _session_handler({"_ref": REF, "name": "avp1", "type": 1, "value_type": "STRING"})
    ) as c:
        r = await c.security.parentalcontrol_avp.get(REF)
        assert r.ref == REF
        assert r.name == "avp1"


async def test_parentalcontrol_avp_find_one() -> None:
    async with _client(
        _session_handler({"result": [{"_ref": REF, "name": "avp1"}], "next_page_id": ""})
    ) as c:
        r = await c.security.parentalcontrol_avp.find_one(name="avp1")
        assert r is not None
        assert r.name == "avp1"


async def test_parentalcontrol_avp_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "avp1"})

    async with _client(handler) as c:
        r = await c.security.parentalcontrol_avp.create(
            {"name": "avp1", "type": 1, "value_type": "STRING"}
        )
        assert r.ref == REF
        body = captured[0].content.decode()
        assert '"avp1"' in body


async def test_parentalcontrol_avp_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": REF, "name": "avp1"})

    async with _client(handler) as c:
        obj = ParentalcontrolAvp(
            name="avp1",
            comment="updated",
            type=1,
            value_type="STRING",
            vendor_id=9,
            user_defined=True,
            uuid="ro-uuid",
        )
        await c.security.parentalcontrol_avp.update(REF, obj)
        body = captured[0].content.decode()
        assert '"uuid"' not in body
        assert '"user_defined"' not in body
        assert '"comment":"updated"' in body


async def test_parentalcontrol_avp_delete() -> None:
    async with _client(_session_handler(REF)) as c:
        assert await c.security.parentalcontrol_avp.delete(REF) == REF
