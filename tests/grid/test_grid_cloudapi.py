# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Grid Cloud API resource tests - 6 resources."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.grid_cloudapi import GridCloudapi
from ibx_nios_sdk.grid.models.grid_cloudapi_cloudstatistics import GridCloudapiCloudstatistics
from ibx_nios_sdk.grid.models.grid_cloudapi_tenant import GridCloudapiTenant
from ibx_nios_sdk.grid.models.grid_cloudapi_vm import GridCloudapiVm
from ibx_nios_sdk.grid.models.grid_cloudapi_vmaddress import GridCloudapiVmaddress
from ibx_nios_sdk.grid.models.grid_member_cloudapi import GridMemberCloudapi
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


# ============================================================= GridCloudapi =====
_CA_REF = "grid:cloudapi/ZG5z:default"
_CA_OBJ = {"_ref": _CA_REF, "allow_api_admins": "ALL", "enable_recycle_bin": True}


async def test_grid_cloudapi_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_CA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_cloudapi.list().all()
        assert results[0].allow_api_admins == "ALL"


async def test_grid_cloudapi_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_CA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi.get(_CA_REF)
        assert obj.enable_recycle_bin is True


async def test_grid_cloudapi_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_CA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi.find_one()
        assert obj is not None


async def test_grid_cloudapi_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_CA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi.create({"allow_api_admins": "ALL"})
        assert obj.allow_api_admins == "ALL"
        assert captured[0].method == "POST"


async def test_grid_cloudapi_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_CA_OBJ)

    async with _client(handler) as c:
        obj = GridCloudapi(allow_api_admins="ALL", uuid="u1")
        await c.grid.grid_cloudapi.update(_CA_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("allow_api_admins") == "ALL"


async def test_grid_cloudapi_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_CA_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_cloudapi.delete(_CA_REF)
        assert _CA_REF in result or result == _CA_REF


# ============================================================= GridCloudapiCloudstatistics =====
_STATS_REF = "grid:cloudapi:cloudstatistics/ZG5z:default"
_STATS_OBJ = {
    "_ref": _STATS_REF,
    "allocated_ip_count": 50,
    "available_ip_count": "200",
    "tenant_count": 5,
}


async def test_grid_cloudapi_cloudstatistics_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_STATS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_cloudapi_cloudstatistics.list().all()
        assert results[0].allocated_ip_count == 50


async def test_grid_cloudapi_cloudstatistics_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_STATS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_cloudstatistics.get(_STATS_REF)
        assert obj.tenant_count == 5


async def test_grid_cloudapi_cloudstatistics_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_STATS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_cloudstatistics.find_one()
        assert obj is not None


async def test_grid_cloudapi_cloudstatistics_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_STATS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_cloudstatistics.create({})
        assert obj.available_ip_count == "200"
        assert captured[0].method == "POST"


async def test_grid_cloudapi_cloudstatistics_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_STATS_OBJ)

    async with _client(handler) as c:
        obj = GridCloudapiCloudstatistics(allocated_ip_count=50, tenant_count=5)
        await c.grid.grid_cloudapi_cloudstatistics.update(_STATS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "allocated_ip_count" not in body
        assert "tenant_count" not in body


async def test_grid_cloudapi_cloudstatistics_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_STATS_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_cloudapi_cloudstatistics.delete(_STATS_REF)
        assert _STATS_REF in result or result == _STATS_REF


# ============================================================= GridCloudapiTenant =====
_TENANT_REF = "grid:cloudapi:tenant/ZG5z:t1"
_TENANT_OBJ = {"_ref": _TENANT_REF, "name": "tenant1", "id": "t-001", "comment": "test"}


async def test_grid_cloudapi_tenant_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_TENANT_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_cloudapi_tenant.list().all()
        assert results[0].name == "tenant1"


async def test_grid_cloudapi_tenant_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_TENANT_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_tenant.get(_TENANT_REF)
        assert obj.id == "t-001"


async def test_grid_cloudapi_tenant_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_TENANT_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_tenant.find_one(name="tenant1")
        assert obj is not None


async def test_grid_cloudapi_tenant_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_TENANT_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_tenant.create({"name": "tenant1"})
        assert obj.name == "tenant1"
        assert captured[0].method == "POST"


async def test_grid_cloudapi_tenant_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_TENANT_OBJ)

    async with _client(handler) as c:
        obj = GridCloudapiTenant(name="tenant1", id="t-001", uuid="u1")
        await c.grid.grid_cloudapi_tenant.update(_TENANT_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "id" not in body
        assert "uuid" not in body
        assert body.get("name") == "tenant1"


async def test_grid_cloudapi_tenant_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_TENANT_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_cloudapi_tenant.delete(_TENANT_REF)
        assert _TENANT_REF in result or result == _TENANT_REF


# ============================================================= GridCloudapiVm =====
_VM_REF = "grid:cloudapi:vm/ZG5z:vm1"
_VM_OBJ = {
    "_ref": _VM_REF,
    "name": "vm1",
    "hostname": "vm1.example.com",
    "id": "vm-001",
    "kernel_id": "k-001",
}


async def test_grid_cloudapi_vm_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_VM_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_cloudapi_vm.list().all()
        assert results[0].name == "vm1"


async def test_grid_cloudapi_vm_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_VM_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_vm.get(_VM_REF)
        assert obj.kernel_id == "k-001"


async def test_grid_cloudapi_vm_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_VM_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_vm.find_one(name="vm1")
        assert obj is not None


async def test_grid_cloudapi_vm_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_VM_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_vm.create({"name": "vm1", "kernel_id": "k-001"})
        assert obj.name == "vm1"
        assert captured[0].method == "POST"


async def test_grid_cloudapi_vm_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_VM_OBJ)

    async with _client(handler) as c:
        obj = GridCloudapiVm(name="vm1", kernel_id="k-001", hostname="vm1.example.com", uuid="u1")
        await c.grid.grid_cloudapi_vm.update(_VM_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "hostname" not in body
        assert "uuid" not in body
        assert body.get("kernel_id") == "k-001"


async def test_grid_cloudapi_vm_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_VM_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_cloudapi_vm.delete(_VM_REF)
        assert _VM_REF in result or result == _VM_REF


# ============================================================= GridCloudapiVmaddress =====
_VMA_REF = "grid:cloudapi:vmaddress/ZG5z:10.0.0.1"
_VMA_OBJ = {
    "_ref": _VMA_REF,
    "vm_id": "vm-001",
    "vm_name": "vm1",
    "address": "10.0.0.1",
    "vm_hostname": "vm1.example.com",
}


async def test_grid_cloudapi_vmaddress_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_VMA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_cloudapi_vmaddress.list().all()
        assert results[0].vm_id == "vm-001"


async def test_grid_cloudapi_vmaddress_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_VMA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_vmaddress.get(_VMA_REF)
        assert obj.address == "10.0.0.1"


async def test_grid_cloudapi_vmaddress_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_VMA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_vmaddress.find_one()
        assert obj is not None


async def test_grid_cloudapi_vmaddress_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_VMA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_cloudapi_vmaddress.create({"cloud_info": {}})
        assert obj.vm_id == "vm-001"
        assert captured[0].method == "POST"


async def test_grid_cloudapi_vmaddress_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_VMA_OBJ)

    async with _client(handler) as c:
        obj = GridCloudapiVmaddress(
            cloud_info={}, vm_id="vm-001", address="10.0.0.1", vm_name="vm1"
        )
        await c.grid.grid_cloudapi_vmaddress.update(_VMA_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "vm_id" not in body
        assert "address" not in body
        assert "vm_name" not in body


async def test_grid_cloudapi_vmaddress_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_VMA_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_cloudapi_vmaddress.delete(_VMA_REF)
        assert _VMA_REF in result or result == _VMA_REF


# ============================================================= GridMemberCloudapi =====
_MCA_REF = "grid:member:cloudapi/ZG5z:m1"
_MCA_OBJ = {
    "_ref": _MCA_REF,
    "member": {"_struct": "dhcpmember", "name": "m1.example.com"},
    "enable_service": True,
    "status": "WORKING",
}


async def test_grid_member_cloudapi_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MCA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_member_cloudapi.list().all()
        assert results[0].member == {"_struct": "dhcpmember", "name": "m1.example.com"}


async def test_grid_member_cloudapi_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MCA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_member_cloudapi.get(_MCA_REF)
        assert obj.enable_service is True


async def test_grid_member_cloudapi_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MCA_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_member_cloudapi.find_one(member="m1.example.com")
        assert obj is not None


async def test_grid_member_cloudapi_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MCA_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_member_cloudapi.create(
            {"member": {"_struct": "dhcpmember", "name": "m1.example.com"}, "enable_service": True}
        )
        assert obj.member == {"_struct": "dhcpmember", "name": "m1.example.com"}
        assert captured[0].method == "POST"


async def test_grid_member_cloudapi_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MCA_OBJ)

    async with _client(handler) as c:
        obj = GridMemberCloudapi(
            member={"_struct": "dhcpmember", "name": "m1.example.com"},
            enable_service=True,
            status="WORKING",
            uuid="u1",
        )
        await c.grid.grid_member_cloudapi.update(_MCA_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "status" not in body
        assert "uuid" not in body
        assert body.get("enable_service") is True


async def test_grid_member_cloudapi_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MCA_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_member_cloudapi.delete(_MCA_REF)
        assert _MCA_REF in result or result == _MCA_REF
