# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordTxtResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_txt import RecordTxt
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


async def test_record_txt_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:txt/ZG5z:example.com/default",
                        "name": "example.com",
                        "text": "v=spf1 include:example.com ~all",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_txt.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.text == "v=spf1 include:example.com ~all"

        params = captured[0].url.params
        assert params["zone"] == "example.com"
        assert "text" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_txt_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:txt/ZG5z:example.com/default",
                "name": "example.com",
                "text": "v=spf1 include:example.com ~all",
                "view": "default",
                "zone": "example.com",
                "comment": "spf record",
            }
        )

    async with _client(handler) as c:
        ref = "record:txt/ZG5z:example.com/default"
        r = await c.dns.record_txt.get(ref)
        assert r.text == "v=spf1 include:example.com ~all"
        assert r.comment == "spf record"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_txt_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:txt/ZG5z:example.com/default",
                        "name": "example.com",
                        "text": "v=spf1 include:example.com ~all",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_txt.find_one(name="example.com")
        assert r is not None
        assert r.text == "v=spf1 include:example.com ~all"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_record_txt_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:txt/NEW:example.com/default",
                "name": "example.com",
                "text": "v=spf1 include:example.com ~all",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_txt.create(
            {
                "name": "example.com",
                "text": "v=spf1 include:example.com ~all",
                "view": "default",
            }
        )
        assert r.text == "v=spf1 include:example.com ~all"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"text"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_record_txt_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:txt/ZG5z:example.com/default",
                "name": "example.com",
                "text": "updated text",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:txt/ZG5z:example.com/default"
        r = RecordTxt(
            name="example.com",
            text="updated text",
            comment="updated",
            creation_time=1700000000,  # RO
            dns_name="example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
            uuid="uuid-123",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_txt.update(ref, r)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_name"' not in body
        assert '"last_queried"' not in body
        assert '"reclaimable"' not in body
        assert '"shared_record_group"' not in body
        assert '"zone"' not in body

        assert '"text":"updated text"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_record_txt_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:txt/ZG5z:example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_txt.delete("record:txt/ZG5z:example.com/default")
        assert result == "record:txt/ZG5z:example.com/default"
