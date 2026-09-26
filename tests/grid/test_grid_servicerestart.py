# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Grid service-restart resource tests - 5 resources."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.grid_servicerestart_group import GridServicerestartGroup
from ibx_nios_sdk.grid.models.grid_servicerestart_group_order import GridServicerestartGroupOrder
from ibx_nios_sdk.grid.models.grid_servicerestart_request import GridServicerestartRequest
from ibx_nios_sdk.grid.models.grid_servicerestart_request_changedobject import (
    GridServicerestartRequestChangedobject,
)
from ibx_nios_sdk.grid.models.grid_servicerestart_status import GridServicerestartStatus
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


# ============================================================= GridServicerestartGroup =====
_SRG_REF = "grid:servicerestart:group/ZG5z:mygroup"
_SRG_OBJ = {
    "_ref": _SRG_REF,
    "name": "mygroup",
    "comment": "test group",
    "service": "DNS",
    "mode": "SEQUENTIAL",
    "is_default": False,
    "uuid": "srg-uuid",
}


async def test_grid_servicerestart_group_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_servicerestart_group.list().all()
        assert results[0].name == "mygroup"


async def test_grid_servicerestart_group_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_group.get(_SRG_REF)
        assert obj.service == "DNS"


async def test_grid_servicerestart_group_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRG_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_group.find_one(name="mygroup")
        assert obj is not None


async def test_grid_servicerestart_group_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRG_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_group.create({"name": "mygroup", "service": "DNS"})
        assert obj.name == "mygroup"
        assert captured[0].method == "POST"


async def test_grid_servicerestart_group_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRG_OBJ)

    async with _client(handler) as c:
        obj = GridServicerestartGroup(
            name="mygroup", service="DNS", is_default=False, uuid="srg-uuid", status="QUEUED"
        )
        await c.grid.grid_servicerestart_group.update(_SRG_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "is_default" not in body
        assert "uuid" not in body
        assert "status" not in body
        assert body.get("name") == "mygroup"


async def test_grid_servicerestart_group_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRG_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_servicerestart_group.delete(_SRG_REF)
        assert _SRG_REF in result or result == _SRG_REF


async def test_grid_servicerestart_group_restart_services() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response({})

    async with _client(handler) as c:
        await c.grid.grid_servicerestart_group.restart_services(
            _SRG_REF,
            services=["DNS"],
            restart_option="RESTART_IF_NEEDED",
        )
        assert captured[0].method == "POST"
        assert "_function=restart" in str(captured[0].url)
        body = json.loads(captured[0].content.decode())
        assert body["services"] == ["DNS"]
        assert body["restart_option"] == "RESTART_IF_NEEDED"


# ============================================================= GridServicerestartStatus =====
_SRS_REF = "grid:servicerestart:status/ZG5z:status1"
_SRS_OBJ = {
    "_ref": _SRS_REF,
    "pending": 3,
    "success": 1,
    "failures": 0,
    "parent": "grid:servicerestart:group/ZG5z:mygroup",
}


async def test_grid_servicerestart_status_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_servicerestart_status.list().all()
        assert results[0].pending == 3


async def test_grid_servicerestart_status_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_status.get(_SRS_REF)
        assert obj.failures == 0


async def test_grid_servicerestart_status_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_status.find_one()
        assert obj is not None


async def test_grid_servicerestart_status_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_status.create({})
        assert obj.pending == 3
        assert captured[0].method == "POST"


async def test_grid_servicerestart_status_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRS_OBJ)

    async with _client(handler) as c:
        obj = GridServicerestartStatus(pending=3, success=1, failures=0)
        await c.grid.grid_servicerestart_status.update(_SRS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "pending" not in body
        assert "success" not in body
        assert "failures" not in body


async def test_grid_servicerestart_status_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRS_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_servicerestart_status.delete(_SRS_REF)
        assert _SRS_REF in result or result == _SRS_REF


# ============================================================= GridServicerestartRequest =====
_SRR_REF = "grid:servicerestart:request/ZG5z:req1"
_SRR_OBJ = {
    "_ref": _SRR_REF,
    "member": "m1.example.com",
    "service": "DNS",
    "state": "QUEUED",
    "result": "PENDING",
    "uuid": "srr-uuid",
}


async def test_grid_servicerestart_request_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRR_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_servicerestart_request.list().all()
        assert results[0].member == "m1.example.com"


async def test_grid_servicerestart_request_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRR_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_request.get(_SRR_REF)
        assert obj.service == "DNS"


async def test_grid_servicerestart_request_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRR_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_request.find_one()
        assert obj is not None


async def test_grid_servicerestart_request_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRR_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_request.create({})
        assert obj.member == "m1.example.com"
        assert captured[0].method == "POST"


async def test_grid_servicerestart_request_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRR_OBJ)

    async with _client(handler) as c:
        obj = GridServicerestartRequest(
            member="m1.example.com", service="DNS", state="QUEUED", uuid="srr-uuid"
        )
        await c.grid.grid_servicerestart_request.update(_SRR_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "member" not in body
        assert "service" not in body
        assert "uuid" not in body


async def test_grid_servicerestart_request_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRR_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_servicerestart_request.delete(_SRR_REF)
        assert _SRR_REF in result or result == _SRR_REF


# ============================================================= GridServicerestartGroupOrder =====
_SRGO_REF = "grid:servicerestart:group:order/ZG5z:order1"
_SRGO_OBJ = {
    "_ref": _SRGO_REF,
    "groups": ["group1", "group2"],
}


async def test_grid_servicerestart_group_order_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRGO_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_servicerestart_group_order.list().all()
        assert results[0].groups == ["group1", "group2"]


async def test_grid_servicerestart_group_order_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRGO_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_group_order.get(_SRGO_REF)
        assert len(obj.groups) == 2  # type: ignore[arg-type]


async def test_grid_servicerestart_group_order_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRGO_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_group_order.find_one()
        assert obj is not None


async def test_grid_servicerestart_group_order_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRGO_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_group_order.create({"groups": ["group1", "group2"]})
        assert obj.groups == ["group1", "group2"]
        assert captured[0].method == "POST"


async def test_grid_servicerestart_group_order_update() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRGO_OBJ)

    async with _client(handler) as c:
        obj = GridServicerestartGroupOrder(groups=["group1", "group2"])
        await c.grid.grid_servicerestart_group_order.update(_SRGO_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert body.get("groups") == ["group1", "group2"]


async def test_grid_servicerestart_group_order_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRGO_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_servicerestart_group_order.delete(_SRGO_REF)
        assert _SRGO_REF in result or result == _SRGO_REF


# ============================================================= GridServicerestartRequestChangedobject =====
_SRCO_REF = "grid:servicerestart:request:changedobject/ZG5z:co1"
_SRCO_OBJ = {
    "_ref": _SRCO_REF,
    "object_name": "myzone.example.com",
    "object_type": "zone_auth",
    "action": "MODIFY",
    "user_name": "admin",
    "uuid": "srco-uuid",
}


async def test_grid_servicerestart_request_changedobject_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRCO_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_servicerestart_request_changedobject.list().all()
        assert results[0].object_name == "myzone.example.com"


async def test_grid_servicerestart_request_changedobject_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRCO_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_request_changedobject.get(_SRCO_REF)
        assert obj.action == "MODIFY"


async def test_grid_servicerestart_request_changedobject_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_SRCO_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_request_changedobject.find_one()
        assert obj is not None


async def test_grid_servicerestart_request_changedobject_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRCO_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_servicerestart_request_changedobject.create({})
        assert obj.object_type == "zone_auth"
        assert captured[0].method == "POST"


async def test_grid_servicerestart_request_changedobject_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_SRCO_OBJ)

    async with _client(handler) as c:
        obj = GridServicerestartRequestChangedobject(
            object_name="myzone.example.com", action="MODIFY", uuid="srco-uuid"
        )
        await c.grid.grid_servicerestart_request_changedobject.update(_SRCO_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "object_name" not in body
        assert "action" not in body
        assert "uuid" not in body


async def test_grid_servicerestart_request_changedobject_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_SRCO_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_servicerestart_request_changedobject.delete(_SRCO_REF)
        assert _SRCO_REF in result or result == _SRCO_REF
