# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for Membercloudsync, Captiveportal, Mastergrid."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.captiveportal import Captiveportal
from ibx_nios_sdk.grid.models.mastergrid import Mastergrid
from ibx_nios_sdk.grid.models.membercloudsync import Membercloudsync
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


# ============================================================= Membercloudsync =====
_MCS_REF = "membercloudsync/ZG5z:m1.example.com"
_MCS_OBJ = {
    "_ref": _MCS_REF,
    "host_name": "m1.example.com",
    "cloud_sync_enabled": True,
    "uuid": "mcs-uuid",
}


async def test_membercloudsync_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MCS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.membercloudsync.list().all()
        assert results[0].cloud_sync_enabled is True


async def test_membercloudsync_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MCS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.membercloudsync.get(_MCS_REF)
        assert obj.host_name == "m1.example.com"


async def test_membercloudsync_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MCS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.membercloudsync.find_one()
        assert obj is not None


async def test_membercloudsync_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MCS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.membercloudsync.create({"cloud_sync_enabled": True})
        assert obj.cloud_sync_enabled is True
        assert captured[0].method == "POST"


async def test_membercloudsync_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MCS_OBJ)

    async with _client(handler) as c:
        obj = Membercloudsync(cloud_sync_enabled=True, host_name="m1.example.com", uuid="mcs-uuid")
        await c.grid.membercloudsync.update(_MCS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "uuid" not in body
        assert body.get("cloud_sync_enabled") is True


async def test_membercloudsync_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MCS_REF)

    async with _client(handler) as c:
        result = await c.grid.membercloudsync.delete(_MCS_REF)
        assert _MCS_REF in result or result == _MCS_REF


# ============================================================= Captiveportal =====
_CP_REF = "captiveportal/ZG5z:cp1"
_CP_OBJ = {
    "_ref": _CP_REF,
    "name": "cp1",
    "company_name": "ACME Corp",
    "service_enabled": True,
    "uuid": "cp-uuid",
}


async def test_captiveportal_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_CP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.captiveportal.list().all()
        assert results[0].company_name == "ACME Corp"


async def test_captiveportal_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_CP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.captiveportal.get(_CP_REF)
        assert obj.service_enabled is True


async def test_captiveportal_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_CP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.captiveportal.find_one()
        assert obj is not None


async def test_captiveportal_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_CP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.captiveportal.create({"company_name": "ACME Corp"})
        assert obj.company_name == "ACME Corp"
        assert captured[0].method == "POST"


async def test_captiveportal_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_CP_OBJ)

    async with _client(handler) as c:
        obj = Captiveportal(company_name="ACME Corp", name="cp1", uuid="cp-uuid")
        await c.grid.captiveportal.update(_CP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "name" not in body
        assert "uuid" not in body
        assert body.get("company_name") == "ACME Corp"


async def test_captiveportal_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_CP_REF)

    async with _client(handler) as c:
        result = await c.grid.captiveportal.delete(_CP_REF)
        assert _CP_REF in result or result == _CP_REF


# ============================================================= Mastergrid =====
_MG_REF = "mastergrid/ZG5z:mg1"
_MG_OBJ = {
    "_ref": _MG_REF,
    "address": "192.168.1.1",
    "enable": True,
    "join_status": "JOINED",
    "uuid": "mg-uuid",
}


async def test_mastergrid_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.mastergrid.list().all()
        assert results[0].address == "192.168.1.1"


async def test_mastergrid_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.mastergrid.get(_MG_REF)
        assert obj.join_status == "JOINED"


async def test_mastergrid_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.mastergrid.find_one()
        assert obj is not None


async def test_mastergrid_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.mastergrid.create({"address": "192.168.1.1", "enable": True})
        assert obj.address == "192.168.1.1"
        assert captured[0].method == "POST"


async def test_mastergrid_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MG_OBJ)

    async with _client(handler) as c:
        obj = Mastergrid(address="192.168.1.1", enable=True, join_status="JOINED", uuid="mg-uuid")
        await c.grid.mastergrid.update(_MG_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "join_status" not in body
        assert "uuid" not in body
        assert body.get("address") == "192.168.1.1"


async def test_mastergrid_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MG_REF)

    async with _client(handler) as c:
        result = await c.grid.mastergrid.delete(_MG_REF)
        assert _MG_REF in result or result == _MG_REF
