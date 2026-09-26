# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordTxtResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecord_txt import SharedrecordTxt
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


async def test_sharedrecord_txt_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:txt/ZG5z:example.com",
                        "name": "example.com",
                        "text": "v=spf1 include:example.com ~all",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_txt.list(shared_record_group="srg-1").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.text == "v=spf1 include:example.com ~all"

        params = captured[0].url.params
        assert params["shared_record_group"] == "srg-1"


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecord:txt/ZG5z:example.com",
                "name": "example.com",
                "text": "v=spf1 include:example.com ~all",
                "shared_record_group": "srg-1",
                "comment": "SPF record",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:txt/ZG5z:example.com"
        r = await c.dns.sharedrecord_txt.get(ref)
        assert r.name == "example.com"
        assert r.text == "v=spf1 include:example.com ~all"
        assert r.comment == "SPF record"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:txt/ZG5z:example.com",
                        "name": "example.com",
                        "text": "v=spf1 include:example.com ~all",
                        "shared_record_group": "srg-1",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_txt.find_one(name="example.com")
        assert r is not None
        assert r.text == "v=spf1 include:example.com ~all"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:txt/NEW:example.com",
                "name": "example.com",
                "text": "v=spf1 include:example.com ~all",
                "shared_record_group": "srg-1",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_txt.create(
            {
                "name": "example.com",
                "text": "v=spf1 include:example.com ~all",
                "shared_record_group": "srg-1",
            }
        )
        assert r.text == "v=spf1 include:example.com ~all"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"text":"v=spf1 include:example.com ~all"' in body
        assert '"shared_record_group":"srg-1"' in body


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:txt/ZG5z:example.com",
                "name": "example.com",
                "text": "updated text",
                "shared_record_group": "srg-1",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:txt/ZG5z:example.com"
        r = SharedrecordTxt(
            name="example.com",
            text="updated text",
            dns_name="example.com.",  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecord_txt.update(ref, r)
        body = captured[0].content.decode()

        assert '"dns_name"' not in body
        assert '"uuid"' not in body
        assert '"text":"updated text"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecord:txt/ZG5z:example.com")

    async with _client(handler) as c:
        result = await c.dns.sharedrecord_txt.delete("sharedrecord:txt/ZG5z:example.com")
        assert result == "sharedrecord:txt/ZG5z:example.com"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:txt/ZG5z:example.com",
                        "name": "example.com",
                        "text": "v=spf1 include:example.com ~all",
                        "shared_record_group": "srg-1",
                        "extattrs": {"Type": {"value": "SPF"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_txt.list().all()
        r = records[0]
        assert r.extattrs is not None
        assert r.extattrs["Type"].value == "SPF"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper
# ---------------------------------------------------------------------------


async def test_sharedrecord_txt_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:txt/ZG5z:example.com",
                "name": "example.com",
                "shared_record_group": "srg-1",
                "extattrs": {"Type": {"value": "SPF"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:txt/ZG5z:example.com"
        await c.dns.sharedrecord_txt.set_extattrs(ref, Type="SPF")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert body_data["extattrs"]["Type"]["value"] == "SPF"
