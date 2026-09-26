# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordSrvResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecord_srv import SharedrecordSrv
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


async def test_sharedrecord_srv_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:srv/ZG5z:_http._tcp.example.com",
                        "name": "_http._tcp.example.com",
                        "port": 80,
                        "priority": 10,
                        "target": "web.example.com",
                        "weight": 100,
                        "shared_record_group": "srg-1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_srv.list(shared_record_group="srg-1").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "_http._tcp.example.com"
        assert r.port == 80
        assert r.priority == 10
        assert r.target == "web.example.com"
        assert r.weight == 100

        params = captured[0].url.params
        assert params["shared_record_group"] == "srg-1"


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecord:srv/ZG5z:_http._tcp.example.com",
                "name": "_http._tcp.example.com",
                "port": 443,
                "priority": 5,
                "target": "secure.example.com",
                "weight": 50,
                "shared_record_group": "srg-1",
                "comment": "HTTPS SRV",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:srv/ZG5z:_http._tcp.example.com"
        r = await c.dns.sharedrecord_srv.get(ref)
        assert r.port == 443
        assert r.priority == 5
        assert r.target == "secure.example.com"
        assert r.comment == "HTTPS SRV"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:srv/ZG5z:_http._tcp.example.com",
                        "name": "_http._tcp.example.com",
                        "port": 80,
                        "priority": 10,
                        "target": "web.example.com",
                        "weight": 100,
                        "shared_record_group": "srg-1",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_srv.find_one(name="_http._tcp.example.com")
        assert r is not None
        assert r.port == 80
        assert r.target == "web.example.com"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:srv/NEW:_http._tcp.example.com",
                "name": "_http._tcp.example.com",
                "port": 80,
                "priority": 10,
                "target": "web.example.com",
                "weight": 100,
                "shared_record_group": "srg-1",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.sharedrecord_srv.create(
            {
                "name": "_http._tcp.example.com",
                "port": 80,
                "priority": 10,
                "target": "web.example.com",
                "weight": 100,
                "shared_record_group": "srg-1",
            }
        )
        assert r.port == 80
        assert r.target == "web.example.com"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"port":80' in body
        assert '"target":"web.example.com"' in body
        assert '"shared_record_group":"srg-1"' in body


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:srv/ZG5z:_http._tcp.example.com",
                "name": "_http._tcp.example.com",
                "port": 8080,
                "priority": 10,
                "target": "web.example.com",
                "weight": 100,
                "shared_record_group": "srg-1",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:srv/ZG5z:_http._tcp.example.com"
        r = SharedrecordSrv(
            name="_http._tcp.example.com",
            port=8080,
            priority=10,
            target="web.example.com",
            weight=100,
            dns_name="_http._tcp.example.com.",  # RO
            dns_target="web.example.com.",  # RO
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecord_srv.update(ref, r)
        body = captured[0].content.decode()

        assert '"dns_name"' not in body
        assert '"dns_target"' not in body
        assert '"uuid"' not in body
        assert '"port":8080' in body
        assert '"target":"web.example.com"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecord:srv/ZG5z:_http._tcp.example.com")

    async with _client(handler) as c:
        result = await c.dns.sharedrecord_srv.delete(
            "sharedrecord:srv/ZG5z:_http._tcp.example.com"
        )
        assert result == "sharedrecord:srv/ZG5z:_http._tcp.example.com"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecord:srv/ZG5z:_http._tcp.example.com",
                        "name": "_http._tcp.example.com",
                        "port": 80,
                        "priority": 10,
                        "target": "web.example.com",
                        "weight": 100,
                        "shared_record_group": "srg-1",
                        "extattrs": {"Service": {"value": "http"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.sharedrecord_srv.list().all()
        r = records[0]
        assert r.extattrs is not None
        assert r.extattrs["Service"].value == "http"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper
# ---------------------------------------------------------------------------


async def test_sharedrecord_srv_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecord:srv/ZG5z:_http._tcp.example.com",
                "name": "_http._tcp.example.com",
                "shared_record_group": "srg-1",
                "extattrs": {"Service": {"value": "http"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecord:srv/ZG5z:_http._tcp.example.com"
        await c.dns.sharedrecord_srv.set_extattrs(ref, Service="http")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert body_data["extattrs"]["Service"]["value"] == "http"
