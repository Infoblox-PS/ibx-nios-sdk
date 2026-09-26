# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordMxResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecord_mx import SharedrecordMx
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(shared_record_group="srg-1")
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:mx/ZG5z:example.com",
                        "name": "example.com",
                        "mail_exchanger": "mail.example.com",
                        "preference": 10,
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_mx.list(shared_record_group="srg-1").all()
        assert len(records) == 1
        r = records[0]
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10

        params = captured[0].url.params
        assert params["shared_record_group"] == "srg-1"


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecord:mx/ZG5z:example.com",
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "shared_record_group": "srg-1",
                "comment": "primary mail",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:mx/ZG5z:example.com"
        r = await c.dns.sharedrecord_mx.get(ref)
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10
        assert r.comment == "primary mail"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:mx/ZG5z:example.com",
                        "name": "example.com",
                        "mail_exchanger": "mail.example.com",
                        "preference": 10,
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_mx.find_one(name="example.com")
        assert r is not None
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:mx/NEW:example.com",
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "shared_record_group": "srg-1",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_mx.create(
            {
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "shared_record_group": "srg-1",
            }
        )
        assert r.mail_exchanger == "mail.example.com"
        assert r.preference == 10

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"mail_exchanger":"mail.example.com"' in body
        assert '"preference":10' in body
        assert '"shared_record_group":"srg-1"' in body


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:mx/ZG5z:example.com",
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 20,
                "shared_record_group": "srg-1",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:mx/ZG5z:example.com"
        r = SharedrecordMx(
            name="example.com",
            mail_exchanger="mail.example.com",
            preference=20,
            comment="updated",
            dns_mail_exchanger="mail.example.com.",  # RO
            dns_name="example.com.",  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecord_mx.update(ref, r)
        body = captured[0].content.decode()

        assert '"dns_mail_exchanger"' not in body
        assert '"dns_name"' not in body
        assert '"uuid"' not in body
        assert '"preference":20' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecord:mx/ZG5z:example.com")

    async with _client(handler) as c:
        result = await c.dns.sharedrecord_mx.delete("sharedrecord:mx/ZG5z:example.com")
        assert result == "sharedrecord:mx/ZG5z:example.com"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:mx/ZG5z:example.com",
                        "name": "example.com",
                        "mail_exchanger": "mail.example.com",
                        "preference": 10,
                        "shared_record_group": "srg-1",
                        "extattrs": {"Priority": {"value": "high"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_mx.list().all()
        r = records[0]
        assert r.extattrs is not None
        assert r.extattrs["Priority"].value == "high"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper
# ---------------------------------------------------------------------------


async def test_sharedrecord_mx_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:mx/ZG5z:example.com",
                "name": "example.com",
                "mail_exchanger": "mail.example.com",
                "preference": 10,
                "shared_record_group": "srg-1",
                "extattrs": {"Priority": {"value": "high"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:mx/ZG5z:example.com"
        await c.dns.sharedrecord_mx.set_extattrs(ref, Priority="high")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert body_data["extattrs"]["Priority"]["value"] == "high"
