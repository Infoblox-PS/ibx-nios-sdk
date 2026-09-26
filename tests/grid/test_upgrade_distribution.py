# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for upgrade and distribution resources."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.distributionschedule import Distributionschedule
from ibx_nios_sdk.grid.models.gmcgroup import Gmcgroup
from ibx_nios_sdk.grid.models.gmcschedule import Gmcschedule
from ibx_nios_sdk.grid.models.upgradegroup import Upgradegroup
from ibx_nios_sdk.grid.models.upgradeschedule import Upgradeschedule
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


# ============================================================= Upgradegroup =====
_UG_REF = "upgradegroup/ZG5z:ug1"
_UG_OBJ = {
    "_ref": _UG_REF,
    "name": "default",
    "comment": "Default upgrade group",
    "upgrade_policy": "SEQUENTIAL",
    "uuid": "ug-uuid",
    "time_zone": "UTC",
}


async def test_upgradegroup_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_UG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.upgradegroup.list().all()
        assert results[0].name == "default"


async def test_upgradegroup_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_UG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.upgradegroup.get(_UG_REF)
        assert obj.upgrade_policy == "SEQUENTIAL"


async def test_upgradegroup_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_UG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.upgradegroup.find_one()
        assert obj is not None


async def test_upgradegroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_UG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.upgradegroup.create({"name": "default"})
        assert obj.name == "default"
        assert captured[0].method == "POST"


async def test_upgradegroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_UG_OBJ)

    async with _client(handler) as c:
        obj = Upgradegroup(name="default", comment="Default", time_zone="UTC", uuid="ug-uuid")
        await c.grid.upgradegroup.update(_UG_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "time_zone" not in body
        assert "uuid" not in body
        assert body.get("name") == "default"


async def test_upgradegroup_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_UG_REF)

    async with _client(handler) as c:
        result = await c.grid.upgradegroup.delete(_UG_REF)
        assert _UG_REF in result or result == _UG_REF


# ============================================================= Upgradeschedule =====
_US_REF = "upgradeschedule/ZG5z:us1"
_US_OBJ = {"_ref": _US_REF, "active": True, "start_time": 1700000000, "time_zone": "UTC"}


async def test_upgradeschedule_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_US_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.upgradeschedule.list().all()
        assert results[0].active is True


async def test_upgradeschedule_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_US_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.upgradeschedule.get(_US_REF)
        assert obj.start_time == 1700000000


async def test_upgradeschedule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_US_OBJ)

    async with _client(handler) as c:
        obj = Upgradeschedule(active=True, start_time=1700000000, time_zone="UTC")
        await c.grid.upgradeschedule.update(_US_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "time_zone" not in body
        assert body.get("active") is True


# ============================================================= Upgradestatus (read-only) =====
_USTA_REF = "upgradestatus/ZG5z:usta1"
_USTA_OBJ = {
    "_ref": _USTA_REF,
    "member": "m1.example.com",
    "current_version": "8.6.0",
    "upgrade_state": "IDLE",
    "grid_state": "IDLE",
}


async def test_upgradestatus_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_USTA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.upgradestatus.list().all()
        assert results[0].member == "m1.example.com"


async def test_upgradestatus_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_USTA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.upgradestatus.get(_USTA_REF)
        assert obj.current_version == "8.6.0"


async def test_upgradestatus_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_USTA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.upgradestatus.find_one()
        assert obj is not None


# ============================================================= Distributionschedule =====
_DS_REF = "distributionschedule/ZG5z:ds1"
_DS_OBJ = {"_ref": _DS_REF, "active": False, "start_time": 1700001000, "time_zone": "UTC"}


async def test_distributionschedule_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.distributionschedule.list().all()
        assert results[0].active is False


async def test_distributionschedule_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.distributionschedule.get(_DS_REF)
        assert obj.start_time == 1700001000


async def test_distributionschedule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_DS_OBJ)

    async with _client(handler) as c:
        obj = Distributionschedule(active=False, start_time=1700001000, time_zone="UTC")
        await c.grid.distributionschedule.update(_DS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "time_zone" not in body
        assert body.get("active") is False


async def test_distributionschedule_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DS_REF)

    async with _client(handler) as c:
        result = await c.grid.distributionschedule.delete(_DS_REF)
        assert _DS_REF in result or result == _DS_REF


# ============================================================= Gmcgroup =====
_GMC_REF = "gmcgroup/ZG5z:gmc1"
_GMC_OBJ = {
    "_ref": _GMC_REF,
    "name": "gmc-group-1",
    "comment": "Primary GMC group",
    "gmc_promotion_policy": "PROMOTE_IF_HA",
    "time_zone": "UTC",
    "uuid": "gmc-uuid",
}


async def test_gmcgroup_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_GMC_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.gmcgroup.list().all()
        assert results[0].name == "gmc-group-1"


async def test_gmcgroup_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_GMC_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.gmcgroup.get(_GMC_REF)
        assert obj.gmc_promotion_policy == "PROMOTE_IF_HA"


async def test_gmcgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_GMC_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.gmcgroup.create({"name": "gmc-group-1"})
        assert obj.name == "gmc-group-1"
        assert captured[0].method == "POST"


async def test_gmcgroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_GMC_OBJ)

    async with _client(handler) as c:
        obj = Gmcgroup(name="gmc-group-1", comment="Primary", time_zone="UTC", uuid="gmc-uuid")
        await c.grid.gmcgroup.update(_GMC_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "time_zone" not in body
        assert "uuid" not in body
        assert body.get("name") == "gmc-group-1"


async def test_gmcgroup_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_GMC_REF)

    async with _client(handler) as c:
        result = await c.grid.gmcgroup.delete(_GMC_REF)
        assert _GMC_REF in result or result == _GMC_REF


# ============================================================= Gmcschedule =====
_GS_REF = "gmcschedule/ZG5z:gs1"
_GS_OBJ = {
    "_ref": _GS_REF,
    "activate_gmc_group_schedule": True,
    "uuid": "gs-uuid",
}


async def test_gmcschedule_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_GS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.gmcschedule.list().all()
        assert results[0].activate_gmc_group_schedule is True


async def test_gmcschedule_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_GS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.gmcschedule.get(_GS_REF)
        assert obj.activate_gmc_group_schedule is True


async def test_gmcschedule_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_GS_OBJ)

    async with _client(handler) as c:
        obj = Gmcschedule(activate_gmc_group_schedule=True, uuid="gs-uuid")
        await c.grid.gmcschedule.update(_GS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("activate_gmc_group_schedule") is True
