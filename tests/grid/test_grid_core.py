# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Grid core resource tests - Grid, GridDhcpproperties, GridDns, GridFiledistribution,
GridThreatprotection, GridThreatinsight, GridDashboard.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.grid import Grid
from ibx_nios_sdk.grid.models.grid_dashboard import GridDashboard
from ibx_nios_sdk.grid.models.grid_dhcpproperties import GridDhcpproperties
from ibx_nios_sdk.grid.models.grid_dns import GridDns
from ibx_nios_sdk.grid.models.grid_filedistribution import GridFiledistribution
from ibx_nios_sdk.grid.models.grid_threatinsight import GridThreatinsight
from ibx_nios_sdk.grid.models.grid_threatprotection import GridThreatprotection
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


# ============================================================= Grid ==========
_GRID_REF = "grid/ZG5z:Infoblox"
_GRID_OBJ = {
    "_ref": _GRID_REF,
    "name": "Infoblox",
    "comment": "main grid",
    "secret": "s3cr3t",
}


async def test_grid_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [_GRID_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid.list().all()
        assert len(results) == 1
        assert results[0].name == "Infoblox"
        assert "name" in captured[0].url.params["_return_fields+"]


async def test_grid_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_GRID_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid.get(_GRID_REF)
        assert r.name == "Infoblox"


async def test_grid_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_GRID_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid.find_one(name="Infoblox")
        assert r is not None
        assert r.name == "Infoblox"


async def test_grid_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_GRID_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid.create({"name": "Infoblox"})
        assert r.name == "Infoblox"
        assert captured[0].method == "POST"


async def test_grid_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_GRID_OBJ)

    async with _client(handler) as c:
        obj = Grid(name="Infoblox", uuid="some-uuid", restart_status="RUNNING")
        await c.grid.grid.update(_GRID_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert "restart_status" not in body
        assert body.get("name") == "Infoblox"


async def test_grid_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_GRID_REF)

    async with _client(handler) as c:
        result = await c.grid.grid.delete(_GRID_REF)
        assert _GRID_REF in result or result == _GRID_REF


async def test_grid_restart_services() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({})

    async with _client(handler) as c:
        await c.grid.grid.restart_services(
            _GRID_REF,
            member_order="SIMULTANEOUSLY",
            restart_option="RESTART_IF_NEEDED",
            services=["DNS"],
        )
        assert captured[0].method == "POST"
        assert "_function=restartservices" in str(captured[0].url)
        body = json.loads(captured[0].content.decode())
        assert body["member_order"] == "SIMULTANEOUSLY"
        assert body["services"] == ["DNS"]


# ============================================================= GridDhcpproperties =====
_DHCPP_REF = "grid:dhcpproperties/ZG5z:default"
_DHCPP_OBJ = {
    "_ref": _DHCPP_REF,
    "authority": True,
    "enable_ddns": False,
}


async def test_grid_dhcpproperties_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DHCPP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_dhcpproperties.list().all()
        assert results[0].authority is True


async def test_grid_dhcpproperties_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DHCPP_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_dhcpproperties.get(_DHCPP_REF)
        assert r.authority is True


async def test_grid_dhcpproperties_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DHCPP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid_dhcpproperties.find_one()
        assert r is not None


async def test_grid_dhcpproperties_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_DHCPP_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_dhcpproperties.create({"authority": True})
        assert r.authority is True
        assert captured[0].method == "POST"


async def test_grid_dhcpproperties_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_DHCPP_OBJ)

    async with _client(handler) as c:
        obj = GridDhcpproperties(authority=True, grid="grid/ZG5z", uuid="u1")
        await c.grid.grid_dhcpproperties.update(_DHCPP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "grid" not in body
        assert "uuid" not in body
        assert body.get("authority") is True


async def test_grid_dhcpproperties_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DHCPP_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_dhcpproperties.delete(_DHCPP_REF)
        assert _DHCPP_REF in result or result == _DHCPP_REF


# ============================================================= GridDns =====
_DNS_REF = "grid:dns/ZG5z:default"
_DNS_OBJ = {"_ref": _DNS_REF, "dnssec_enabled": False, "forward_only": True}


async def test_grid_dns_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DNS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_dns.list().all()
        assert results[0].dnssec_enabled is False


async def test_grid_dns_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DNS_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_dns.get(_DNS_REF)
        assert r.forward_only is True


async def test_grid_dns_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DNS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid_dns.find_one()
        assert r is not None


async def test_grid_dns_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_DNS_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_dns.create({"forward_only": True})
        assert r.forward_only is True
        assert captured[0].method == "POST"


async def test_grid_dns_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_DNS_OBJ)

    async with _client(handler) as c:
        obj = GridDns(forward_only=True, uuid="u1")
        await c.grid.grid_dns.update(_DNS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("forward_only") is True


async def test_grid_dns_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DNS_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_dns.delete(_DNS_REF)
        assert _DNS_REF in result or result == _DNS_REF


# ============================================================= GridFiledistribution =====
_FD_REF = "grid:filedistribution/ZG5z:default"
_FD_OBJ = {"_ref": _FD_REF, "allow_uploads": True, "storage_limit": 1024}


async def test_grid_filedistribution_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_FD_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_filedistribution.list().all()
        assert results[0].allow_uploads is True


async def test_grid_filedistribution_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_FD_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_filedistribution.get(_FD_REF)
        assert r.storage_limit == 1024


async def test_grid_filedistribution_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_FD_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid_filedistribution.find_one()
        assert r is not None


async def test_grid_filedistribution_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_FD_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_filedistribution.create({"allow_uploads": True})
        assert r.allow_uploads is True
        assert captured[0].method == "POST"


async def test_grid_filedistribution_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_FD_OBJ)

    async with _client(handler) as c:
        obj = GridFiledistribution(allow_uploads=True, name="grid-fd", uuid="u1", current_usage=50)
        await c.grid.grid_filedistribution.update(_FD_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "name" not in body
        assert "uuid" not in body
        assert "current_usage" not in body
        assert body.get("allow_uploads") is True


async def test_grid_filedistribution_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_FD_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_filedistribution.delete(_FD_REF)
        assert _FD_REF in result or result == _FD_REF


# ============================================================= GridThreatprotection =====
_TP_REF = "grid:threatprotection/ZG5z:default"
_TP_OBJ = {
    "_ref": _TP_REF,
    "enable_auto_download": True,
    "grid_name": "Infoblox",
    "uuid": "tp-uuid",
}


async def test_grid_threatprotection_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_TP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_threatprotection.list().all()
        assert results[0].enable_auto_download is True


async def test_grid_threatprotection_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_TP_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_threatprotection.get(_TP_REF)
        assert r.grid_name == "Infoblox"


async def test_grid_threatprotection_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_TP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid_threatprotection.find_one()
        assert r is not None


async def test_grid_threatprotection_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_TP_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_threatprotection.create({"enable_auto_download": True})
        assert r.enable_auto_download is True
        assert captured[0].method == "POST"


async def test_grid_threatprotection_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_TP_OBJ)

    async with _client(handler) as c:
        obj = GridThreatprotection(enable_auto_download=True, grid_name="Infoblox", uuid="tp-uuid")
        await c.grid.grid_threatprotection.update(_TP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "grid_name" not in body
        assert "uuid" not in body
        assert body.get("enable_auto_download") is True


async def test_grid_threatprotection_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_TP_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_threatprotection.delete(_TP_REF)
        assert _TP_REF in result or result == _TP_REF


# ============================================================= GridThreatinsight =====
_TI_REF = "grid:threatinsight/ZG5z:default"
_TI_OBJ = {
    "_ref": _TI_REF,
    "enable_auto_download": True,
    "name": "Infoblox",
    "uuid": "ti-uuid",
}


async def test_grid_threatinsight_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_TI_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_threatinsight.list().all()
        assert results[0].enable_auto_download is True


async def test_grid_threatinsight_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_TI_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_threatinsight.get(_TI_REF)
        assert r.name == "Infoblox"


async def test_grid_threatinsight_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_TI_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid_threatinsight.find_one()
        assert r is not None


async def test_grid_threatinsight_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_TI_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_threatinsight.create({"enable_auto_download": True})
        assert r.enable_auto_download is True
        assert captured[0].method == "POST"


async def test_grid_threatinsight_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_TI_OBJ)

    async with _client(handler) as c:
        obj = GridThreatinsight(enable_auto_download=True, name="Infoblox", uuid="ti-uuid")
        await c.grid.grid_threatinsight.update(_TI_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "name" not in body
        assert "uuid" not in body
        assert body.get("enable_auto_download") is True


async def test_grid_threatinsight_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_TI_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_threatinsight.delete(_TI_REF)
        assert _TI_REF in result or result == _TI_REF


# ============================================================= GridDashboard =====
_DASH_REF = "grid:dashboard/ZG5z:default"
_DASH_OBJ = {
    "_ref": _DASH_REF,
    "rpz_blocked_hit_critical_threshold": 100,
    "uuid": "dash-uuid",
}


async def test_grid_dashboard_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DASH_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_dashboard.list().all()
        assert results[0].rpz_blocked_hit_critical_threshold == 100


async def test_grid_dashboard_get() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DASH_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_dashboard.get(_DASH_REF)
        assert r.rpz_blocked_hit_critical_threshold == 100


async def test_grid_dashboard_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_DASH_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        r = await c.grid.grid_dashboard.find_one()
        assert r is not None


async def test_grid_dashboard_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_DASH_OBJ)

    async with _client(handler) as c:
        r = await c.grid.grid_dashboard.create({"rpz_blocked_hit_critical_threshold": 100})
        assert r.rpz_blocked_hit_critical_threshold == 100
        assert captured[0].method == "POST"


async def test_grid_dashboard_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(_DASH_OBJ)

    async with _client(handler) as c:
        obj = GridDashboard(rpz_blocked_hit_critical_threshold=100, uuid="dash-uuid")
        await c.grid.grid_dashboard.update(_DASH_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "uuid" not in body
        assert body.get("rpz_blocked_hit_critical_threshold") == 100


async def test_grid_dashboard_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_DASH_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_dashboard.delete(_DASH_REF)
        assert _DASH_REF in result or result == _DASH_REF
