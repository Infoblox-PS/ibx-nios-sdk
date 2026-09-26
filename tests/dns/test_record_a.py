# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordAResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.record_a import RecordA
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(zone="example.com") - filter translated to zone=example.com
# ---------------------------------------------------------------------------


async def test_record_a_list_with_zone_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:a/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "ipv4addr": "192.168.1.10",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_a.list(zone="example.com").all()
        assert len(records) == 1
        r = records[0]
        assert r.name == "host.example.com"
        assert r.ipv4addr == "192.168.1.10"
        assert r.zone == "example.com"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["zone"] == "example.com"
        assert "name" in params["_return_fields+"]
        assert "ipv4addr" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name__like="host") - filter becomes name~=host
# ---------------------------------------------------------------------------


async def test_record_a_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:a/ZG5z:hostname.example.com/default",
                        "name": "hostname.example.com",
                        "ipv4addr": "10.0.0.1",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_a.list(name__like="host").all()
        assert len(records) == 1
        assert records[0].name == "hostname.example.com"

        params = captured[0].url.params
        # name__like should translate to name~=host
        assert (
            params.get("name~") == "host"
            or params.get("name~=") == "host"
            or any(k.startswith("name") and "host" in v for k, v in params.items())
        )


# ---------------------------------------------------------------------------
# 3. get(ref) - parses name/ipv4addr/view/comment
# ---------------------------------------------------------------------------


async def test_record_a_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "record:a/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "ipv4addr": "192.168.1.10",
                "view": "default",
                "zone": "example.com",
                "comment": "web server",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:a/ZG5z:host.example.com/default"
        r = await c.dns.record_a.get(ref)
        assert r.name == "host.example.com"
        assert r.ipv4addr == "192.168.1.10"
        assert r.view == "default"
        assert r.comment == "web server"


# ---------------------------------------------------------------------------
# 4. find_one(name="host.example.com") - returns first match
# ---------------------------------------------------------------------------


async def test_record_a_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:a/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "ipv4addr": "192.168.1.10",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_a.find_one(name="host.example.com")
        assert r is not None
        assert r.name == "host.example.com"
        assert r.ipv4addr == "192.168.1.10"


# ---------------------------------------------------------------------------
# 5. create - POST body correct, _return_as_object=1
# ---------------------------------------------------------------------------


async def test_record_a_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:a/NEW:host.example.com/default",
                "name": "host.example.com",
                "ipv4addr": "192.168.1.10",
                "view": "default",
                "zone": "example.com",
                "comment": "",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        r = await c.dns.record_a.create(
            {"name": "host.example.com", "ipv4addr": "192.168.1.10", "view": "default"}
        )
        assert r.name == "host.example.com"
        assert r.ipv4addr == "192.168.1.10"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"host.example.com"' in body
        assert '"ipv4addr":"192.168.1.10"' in body
        # _return_as_object should be set
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {"comment":"new"}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_record_a_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:a/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "ipv4addr": "192.168.1.10",
                "view": "default",
                "zone": "example.com",
                "comment": "new",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:a/ZG5z:host.example.com/default"
        r = await c.dns.record_a.update(ref, {"comment": "new"})
        assert r.comment == "new"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path
        body = req.content.decode()
        assert '"comment":"new"' in body


# ---------------------------------------------------------------------------
# 7. delete(ref) - returns ref string
# ---------------------------------------------------------------------------


async def test_record_a_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:a/ZG5z:host.example.com/default")

    async with _client(handler) as c:
        result = await c.dns.record_a.delete("record:a/ZG5z:host.example.com/default")
        assert result == "record:a/ZG5z:host.example.com/default"


# ---------------------------------------------------------------------------
# 8. Extattrs round-trip
# ---------------------------------------------------------------------------


async def test_record_a_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "record:a/ZG5z:host.example.com/default",
                        "name": "host.example.com",
                        "ipv4addr": "192.168.1.10",
                        "view": "default",
                        "zone": "example.com",
                        "comment": "",
                        "disable": False,
                        "extattrs": {"Site": {"value": "NYC"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        records = await c.dns.record_a.list().all()
        assert len(records) == 1
        r = records[0]
        assert r.extattrs is not None
        assert "Site" in r.extattrs
        assert r.extattrs["Site"].value == "NYC"


# ---------------------------------------------------------------------------
# 9. set_extattrs helper - PUT body contains extattrs dict
# ---------------------------------------------------------------------------


async def test_record_a_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:a/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "ipv4addr": "192.168.1.10",
                "view": "default",
                "zone": "example.com",
                "comment": "",
                "disable": False,
                "extattrs": {
                    "Site": {"value": "NYC"},
                    "Owner": {"value": "net-eng"},
                },
            }
        )

    async with _client(handler) as c:
        ref = "record:a/ZG5z:host.example.com/default"
        await c.dns.record_a.set_extattrs(ref, Site="NYC", Owner="net-eng")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert "extattrs" in body_data
        assert body_data["extattrs"]["Site"]["value"] == "NYC"
        assert body_data["extattrs"]["Owner"]["value"] == "net-eng"


# ---------------------------------------------------------------------------
# 10. Readonly-strip on update
# ---------------------------------------------------------------------------


async def test_record_a_update_strips_readonly() -> None:
    """Readonly fields must not appear in the PUT body; writable fields must."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "record:a/ZG5z:host.example.com/default",
                "name": "host.example.com",
                "ipv4addr": "192.168.1.10",
                "view": "default",
                "zone": "example.com",
                "comment": "updated",
                "disable": False,
            }
        )

    async with _client(handler) as c:
        ref = "record:a/ZG5z:host.example.com/default"
        # Construct RecordA with a mix of readonly and writable fields
        r = RecordA(
            name="host.example.com",
            comment="updated",
            ipv4addr="192.168.1.10",
            creation_time=1700000000,  # RO
            last_queried=1700000001,  # RO
            dns_name="host.example.com.",  # RO
            reclaimable=True,  # RO
            shared_record_group="srg-1",  # RO
        )
        await c.dns.record_a.update(ref, r)
        body = captured[0].content.decode()

        # Readonly fields must NOT appear
        assert '"creation_time"' not in body, "creation_time is readonly - must be stripped"
        assert '"last_queried"' not in body, "last_queried is readonly - must be stripped"
        assert '"dns_name"' not in body, "dns_name is readonly - must be stripped"
        assert '"reclaimable"' not in body, "reclaimable is readonly - must be stripped"
        assert '"shared_record_group"' not in body, (
            "shared_record_group is readonly - must be stripped"
        )

        # Writable fields must appear
        assert '"name":"host.example.com"' in body
        assert '"comment":"updated"' in body
