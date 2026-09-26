# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordAliasResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_alias import RecordAlias
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


async def test_record_alias_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:alias/ZG5z:alias.example.com/default",
                        "name": "alias.example.com",
                        "target_name": "target.example.com",
                        "target_type": "A",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_alias.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "alias.example.com"
        assert r.target_name == "target.example.com"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name__like="alias")
# ---------------------------------------------------------------------------


async def test_record_alias_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:alias/ZG5z:alias.example.com/default",
                        "name": "alias.example.com",
                        "target_name": "target.example.com",
                        "target_type": "A",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_alias.list(name__like="alias").all()
        assert len(records) == 1
        assert records[0].name == "alias.example.com"

        params = captured[0].url.params
        assert any(k.startswith("name") and "alias" in v for k, v in params.items())


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_alias_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:alias/ZG5z:alias.example.com/default",
                "name": "alias.example.com",
                "target_name": "target.example.com",
                "target_type": "A",
                "view": "default",
                "zone": "example.com",
                "comment": "alias record",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_alias.get("record:alias/ZG5z:alias.example.com/default")
        assert r.name == "alias.example.com"
        assert r.target_name == "target.example.com"
        assert r.comment == "alias record"


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_alias_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:alias/ZG5z:alias.example.com/default",
                        "name": "alias.example.com",
                        "target_name": "target.example.com",
                        "target_type": "A",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_alias.find_one(name="alias.example.com")
        assert r is not None
        assert r.name == "alias.example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_alias_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:alias/NEW:alias.example.com/default",
                "name": "alias.example.com",
                "target_name": "target.example.com",
                "target_type": "A",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_alias.create(
            {"name": "alias.example.com", "target_name": "target.example.com", "view": "default"}
        )
        assert r.name == "alias.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"alias.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_alias_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:alias/ZG5z:alias.example.com/default",
                "name": "alias.example.com",
                "target_name": "target.example.com",
                "target_type": "A",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:alias/ZG5z:alias.example.com/default"
        r_obj = RecordAlias(
            name="alias.example.com",
            comment="updated",
            dns_name="alias.example.com.",  # RO
            dns_target_name="target.example.com.",  # RO
            last_queried=1700000000,  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_alias.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"dns_name"' not in body
        assert '"dns_target_name"' not in body
        assert '"last_queried"' not in body
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"name":"alias.example.com"' in body
        assert '"comment":"updated"' in body
