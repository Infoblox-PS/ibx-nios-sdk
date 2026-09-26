# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for misc resources: GridMaxminddbinfo, Natgroup, Restartservicestatus, Extensibleattributedef."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.extensibleattributedef import Extensibleattributedef
from ibx_nios_sdk.grid.models.natgroup import Natgroup
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ============================================================= GridMaxminddbinfo =====
_MM_REF = "grid:maxminddbinfo/ZG5z:mm1"
_MM_OBJ = {
    "_ref": _MM_REF,
    "member": "m1.example.com",
    "database_type": "GeoIP2-City",
    "topology_type": "CITY",
    "deployment_time": 1700000000,
    "uuid": "mm-uuid",
}


async def test_grid_maxminddbinfo_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MM_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_maxminddbinfo.list().all()
        assert results[0].member == "m1.example.com"


async def test_grid_maxminddbinfo_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MM_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_maxminddbinfo.get(_MM_REF)
        assert obj.database_type == "GeoIP2-City"


async def test_grid_maxminddbinfo_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MM_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_maxminddbinfo.find_one()
        assert obj is not None


# ============================================================= Natgroup =====
_NG_REF = "natgroup/ZG5z:ng1"
_NG_OBJ = {"_ref": _NG_REF, "name": "nat-group-1", "comment": "Primary NAT", "uuid": "ng-uuid"}


async def test_natgroup_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_NG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.natgroup.list().all()
        assert results[0].name == "nat-group-1"


async def test_natgroup_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_NG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.natgroup.get(_NG_REF)
        assert obj.comment == "Primary NAT"


async def test_natgroup_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_NG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.natgroup.find_one()
        assert obj is not None


async def test_natgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_NG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.natgroup.create({"name": "nat-group-1"})
        assert obj.name == "nat-group-1"
        assert captured[0].method == "POST"


async def test_natgroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_NG_OBJ)

    async with _client(handler) as c:
        obj = Natgroup(name="nat-group-1", comment="Primary NAT", uuid="ng-uuid")
        await c.grid.natgroup.update(_NG_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("name") == "nat-group-1"


async def test_natgroup_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_NG_REF)

    async with _client(handler) as c:
        result = await c.grid.natgroup.delete(_NG_REF)
        assert _NG_REF in result or result == _NG_REF


# ============================================================= Restartservicestatus =====
_RSS_REF = "restartservicestatus/ZG5z:rss1"
_RSS_OBJ = {
    "_ref": _RSS_REF,
    "member": "m1.example.com",
    "dhcp_status": "NO_RESTART_NEEDED",
    "dns_status": "RESTART_NEEDED",
    "reporting_status": "NO_RESTART_NEEDED",
    "uuid": "rss-uuid",
}


async def test_restartservicestatus_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_RSS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.restartservicestatus.list().all()
        assert results[0].member == "m1.example.com"


async def test_restartservicestatus_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_RSS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.restartservicestatus.get(_RSS_REF)
        assert obj.dns_status == "RESTART_NEEDED"


async def test_restartservicestatus_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_RSS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.restartservicestatus.find_one()
        assert obj is not None


# ============================================================= Extensibleattributedef =====
_EAD_REF = "extensibleattributedef/ZG5z:ead1"
_EAD_OBJ = {
    "_ref": _EAD_REF,
    "name": "Site",
    "type": "STRING",
    "comment": "Site attribute",
    "flags": "",
    "namespace": "NETMRI",
    "uuid": "ead-uuid",
}


async def test_extensibleattributedef_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_EAD_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.extensibleattributedef.list().all()
        assert results[0].name == "Site"
        assert results[0].type_ == "STRING"


async def test_extensibleattributedef_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_EAD_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.extensibleattributedef.get(_EAD_REF)
        assert obj.comment == "Site attribute"


async def test_extensibleattributedef_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_EAD_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.extensibleattributedef.find_one()
        assert obj is not None


async def test_extensibleattributedef_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_EAD_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.extensibleattributedef.create({"name": "Site", "type": "STRING"})
        assert obj.name == "Site"
        assert captured[0].method == "POST"


async def test_extensibleattributedef_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_EAD_OBJ)

    async with _client(handler) as c:
        obj = Extensibleattributedef(
            name="Site",
            type="STRING",
            comment="Site attribute",
            namespace="NETMRI",
            uuid="ead-uuid",
        )
        await c.grid.extensibleattributedef.update(_EAD_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "namespace" not in body
        assert "uuid" not in body
        assert body.get("name") == "Site"


async def test_extensibleattributedef_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_EAD_REF)

    async with _client(handler) as c:
        result = await c.grid.extensibleattributedef.delete(_EAD_REF)
        assert _EAD_REF in result or result == _EAD_REF
