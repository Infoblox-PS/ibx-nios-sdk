# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordSrvResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_srv import RecordSrv
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


async def test_record_srv_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:srv/ZG5z:_sip._tcp.example.com/default",
                        "name": "_sip._tcp.example.com",
                        "port": 5060,
                        "priority": 10,
                        "target": "sip.example.com",
                        "weight": 20,
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_srv.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "_sip._tcp.example.com"
        assert r.port == 5060
        assert r.target == "sip.example.com"

        params = captured[0].url.params
        assert params["zone"] == "example.com"
        assert "port" in params["_return_fields+"]
        assert "target" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_record_srv_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:srv/ZG5z:_sip._tcp.example.com/default",
                "name": "_sip._tcp.example.com",
                "port": 5060,
                "priority": 10,
                "target": "sip.example.com",
                "weight": 20,
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        ref = "record:srv/ZG5z:_sip._tcp.example.com/default"
        r = await c.dns.record_srv.get(ref)
        assert r.port == 5060
        assert r.priority == 10
        assert r.target == "sip.example.com"
        assert r.weight == 20


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_record_srv_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:srv/ZG5z:_sip._tcp.example.com/default",
                        "name": "_sip._tcp.example.com",
                        "port": 5060,
                        "priority": 10,
                        "target": "sip.example.com",
                        "weight": 20,
                        "view": "default",
                        "zone": "example.com",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_srv.find_one(name="_sip._tcp.example.com")
        assert r is not None
        assert r.target == "sip.example.com"
        assert r.port == 5060


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_record_srv_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:srv/NEW:_sip._tcp.example.com/default",
                "name": "_sip._tcp.example.com",
                "port": 5060,
                "priority": 10,
                "target": "sip.example.com",
                "weight": 20,
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_srv.create(
            {
                "name": "_sip._tcp.example.com",
                "port": 5060,
                "priority": 10,
                "target": "sip.example.com",
                "weight": 20,
                "view": "default",
            }
        )
        assert r.port == 5060
        assert r.target == "sip.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"port":5060' in body
        assert '"target":"sip.example.com"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_record_srv_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:srv/ZG5z:_sip._tcp.example.com/default",
                "name": "_sip._tcp.example.com",
                "port": 5061,
                "priority": 20,
                "target": "sip2.example.com",
                "weight": 10,
                "view": "default",
                "zone": "example.com",
            }
        )

    async with _client(handler) as c:
        ref = "record:srv/ZG5z:_sip._tcp.example.com/default"
        r = RecordSrv(
            name="_sip._tcp.example.com",
            port=5061,
            priority=20,
            target="sip2.example.com",
            weight=10,
            creation_time=1700000000,  # RO
            dns_name="_sip._tcp.example.com.",  # RO
            dns_target="sip2.example.com.",  # RO
            last_queried=1700000001,  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
            zone="example.com",  # RO
        )
        await c.dns.record_srv.update(ref, r)
        body = captured[0].content.decode()

        assert '"creation_time"' not in body
        assert '"dns_name"' not in body
        assert '"dns_target"' not in body
        assert '"last_queried"' not in body
        assert '"reclaimable"' not in body
        assert '"shared_record_group"' not in body
        assert '"zone"' not in body

        assert '"port":5061' in body
        assert '"target":"sip2.example.com"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_record_srv_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:srv/ZG5z:_sip._tcp.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_srv.delete("record:srv/ZG5z:_sip._tcp.example.com/default")
        assert result == "record:srv/ZG5z:_sip._tcp.example.com/default"
