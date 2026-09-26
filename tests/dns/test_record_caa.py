# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordCaaResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_caa import RecordCaa
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


async def test_record_caa_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:caa/ZG5z:example.com/default",
                        "name": "example.com",
                        "ca_flag": 0,
                        "ca_tag": "issue",
                        "ca_value": "letsencrypt.org",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_caa.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "example.com"
        assert r.ca_flag == 0
        assert r.ca_tag == "issue"
        assert r.ca_value == "letsencrypt.org"

        params = captured[0].url.params
        assert params["zone"] == "example.com"


# ---------------------------------------------------------------------------
# 2. list(name__like="example")
# ---------------------------------------------------------------------------


async def test_record_caa_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:caa/ZG5z:example.com/default",
                        "name": "example.com",
                        "ca_flag": 0,
                        "ca_tag": "issue",
                        "ca_value": "letsencrypt.org",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_caa.list(name__like="example").all()
        assert len(records) == 1
        assert records[0].name == "example.com"


# ---------------------------------------------------------------------------
# 3. get(ref)
# ---------------------------------------------------------------------------


async def test_record_caa_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:caa/ZG5z:example.com/default",
                "name": "example.com",
                "ca_flag": 0,
                "ca_tag": "issue",
                "ca_value": "letsencrypt.org",
                "view": "default",
                "zone": "example.com",
                "comment": "caa record",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_caa.get("record:caa/ZG5z:example.com/default")
        assert r.name == "example.com"
        assert r.ca_tag == "issue"
        assert r.comment == "caa record"


# ---------------------------------------------------------------------------
# 4. find_one
# ---------------------------------------------------------------------------


async def test_record_caa_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:caa/ZG5z:example.com/default",
                        "name": "example.com",
                        "ca_flag": 0,
                        "ca_tag": "issue",
                        "ca_value": "letsencrypt.org",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_caa.find_one(name="example.com")
        assert r is not None
        assert r.name == "example.com"


# ---------------------------------------------------------------------------
# 5. create
# ---------------------------------------------------------------------------


async def test_record_caa_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:caa/NEW:example.com/default",
                "name": "example.com",
                "ca_flag": 0,
                "ca_tag": "issue",
                "ca_value": "letsencrypt.org",
                "view": "default",
                "zone": "example.com",
                "comment": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_caa.create(
            {
                "name": "example.com",
                "ca_flag": 0,
                "ca_tag": "issue",
                "ca_value": "letsencrypt.org",
            }
        )
        assert r.name == "example.com"

        req = captured[0]
        assert req.method == "POST"
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update - readonly strip
# ---------------------------------------------------------------------------


async def test_record_caa_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:caa/ZG5z:example.com/default",
                "name": "example.com",
                "ca_flag": 0,
                "ca_tag": "issue",
                "ca_value": "letsencrypt.org",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "record:caa/ZG5z:example.com/default"
        r_obj = RecordCaa(
            name="example.com",
            comment="updated",
            creation_time=1700000000,  # RO
            dns_name="example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            uuid="some-uuid",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_caa.update(ref, r_obj)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_name"' not in body
        assert '"reclaimable"' not in body
        assert '"uuid"' not in body
        assert '"zone"' not in body
        assert '"name":"example.com"' in body
        assert '"comment":"updated"' in body
