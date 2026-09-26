# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordMxResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_mx import RecordMx
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(zone="example.com")
# ---------------------------------------------------------------------------


async def test_record_mx_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:mx/ZG5z:example.com/default",
                        "name": "example.com",
                        "mail_exchanger": "mail.example.com",
                        "preference": 10,
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_mx.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10

        params = captured[0].url.params
        assert params["zone"] == "example.com"
        assert "mail_exchanger" in params["_return_fields+"]
        assert "preference" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_mx_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:mx/ZG5z:example.com/default",
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "view": "default",
                "zone": "example.com",
                "comment": "primary mx",
            }
        )

    async with _client(handler) as c:
        ref = "record:mx/ZG5z:example.com/default"
        r = await c.dns.record_mx.get(ref)
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10
        assert r.comment == "primary mx"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_mx_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:mx/ZG5z:example.com/default",
                        "name": "example.com",
                        "mail_exchanger": "mail.example.com",
                        "preference": 10,
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_mx.find_one(name="example.com")
        assert r is not None
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_record_mx_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:mx/NEW:example.com/default",
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_mx.create(
            {
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "view": "default",
            }
        )
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"mail_exchanger":"mail.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_record_mx_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:mx/ZG5z:example.com/default",
                "name": "example.com",
                "mail_exchanger": "mail2.example.com",
                "preference": 20,
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:mx/ZG5z:example.com/default"
        r = RecordMx(
            name="example.com",
            mail_exchanger="mail2.example.com",
            preference=20,
            comment="updated",
            creation_time=1700000000,  # RO
            dns_mail_exchanger="mail2.example.com.",  # RO
            dns_name="example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_mx.update(ref, r)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_mail_exchanger"' not in body
        assert '"dns_name"' not in body
        assert '"last_queried"' not in body
        assert '"reclaimable"' not in body
        assert '"shared_record_group"' not in body
        assert '"zone"' not in body

        assert '"mail_exchanger":"mail2.example.com"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_record_mx_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:mx/ZG5z:example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_mx.delete("record:mx/ZG5z:example.com/default")
        assert result == "record:mx/ZG5z:example.com/default"
