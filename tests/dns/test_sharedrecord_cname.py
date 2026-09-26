# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordCnameResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecord_cname import SharedrecordCname
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


async def test_sharedrecord_cname_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:cname/ZG5z:alias.example.com",
                        "name": "alias.example.com",
                        "canonical": "target.example.com",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_cname.list(shared_record_group="srg-1").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "alias.example.com"
        assert r.canonical == "target.example.com"

        params = captured[0].url.params
        assert params["shared_record_group"] == "srg-1"


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecord:cname/ZG5z:alias.example.com",
                "name": "alias.example.com",
                "canonical": "target.example.com",
                "shared_record_group": "srg-1",
                "comment": "my cname",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:cname/ZG5z:alias.example.com"
        r = await c.dns.sharedrecord_cname.get(ref)
        assert r.name == "alias.example.com"
        assert r.canonical == "target.example.com"
        assert r.comment == "my cname"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:cname/ZG5z:alias.example.com",
                        "name": "alias.example.com",
                        "canonical": "target.example.com",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_cname.find_one(name="alias.example.com")
        assert r is not None
        assert r.canonical == "target.example.com"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:cname/NEW:alias.example.com",
                "name": "alias.example.com",
                "canonical": "target.example.com",
                "shared_record_group": "srg-1",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_cname.create(
            {
                "name": "alias.example.com",
                "canonical": "target.example.com",
                "shared_record_group": "srg-1",
            }
        )
        assert r.canonical == "target.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"canonical":"target.example.com"' in body
        assert '"shared_record_group":"srg-1"' in body


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:cname/ZG5z:alias.example.com",
                "name": "alias.example.com",
                "canonical": "target.example.com",
                "shared_record_group": "srg-1",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:cname/ZG5z:alias.example.com"
        r = SharedrecordCname(
            name="alias.example.com",
            canonical="target.example.com",
            comment="updated",
            dns_canonical="target.example.com.",  # RO
            dns_name="alias.example.com.",  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecord_cname.update(ref, r)
        body = captured[0].content.decode()

        assert '"dns_canonical"' not in body
        assert '"dns_name"' not in body
        assert '"uuid"' not in body
        assert '"canonical":"target.example.com"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecord:cname/ZG5z:alias.example.com")

    async with _client(handler) as c:
        result = await c.dns.sharedrecord_cname.delete("sharedrecord:cname/ZG5z:alias.example.com")
        assert result == "sharedrecord:cname/ZG5z:alias.example.com"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:cname/ZG5z:alias.example.com",
                        "name": "alias.example.com",
                        "canonical": "target.example.com",
                        "shared_record_group": "srg-1",
                        "extattrs": {"Env": {"value": "prod"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_cname.list().all()
        r = records[0]
        assert r.extattrs is not None
        assert r.extattrs["Env"].value == "prod"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper
# ---------------------------------------------------------------------------


async def test_sharedrecord_cname_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:cname/ZG5z:alias.example.com",
                "name": "alias.example.com",
                "canonical": "target.example.com",
                "shared_record_group": "srg-1",
                "extattrs": {"Env": {"value": "prod"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:cname/ZG5z:alias.example.com"
        await c.dns.sharedrecord_cname.set_extattrs(ref, Env="prod")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert body_data["extattrs"]["Env"]["value"] == "prod"
