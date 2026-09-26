# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Member resource tests - 9 resources."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.member import Member
from ibx_nios_sdk.grid.models.member_dhcpproperties import MemberDhcpproperties
from ibx_nios_sdk.grid.models.member_dns import MemberDns
from ibx_nios_sdk.grid.models.member_filedistribution import MemberFiledistribution
from ibx_nios_sdk.grid.models.member_license import MemberLicense
from ibx_nios_sdk.grid.models.member_parentalcontrol import MemberParentalcontrol
from ibx_nios_sdk.grid.models.member_threatinsight import MemberThreatinsight
from ibx_nios_sdk.grid.models.member_threatprotection import MemberThreatprotection
from ibx_nios_sdk.grid.models.memberdfp import Memberdfp
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


# ============================================================= Member =====
_MBR_REF = "member/ZG5z:m1.example.com"
_MBR_OBJ = {
    "_ref": _MBR_REF,
    "host_name": "m1.example.com",
    "config_addr_type": "IPV4",
    "platform": "VNIOS",
    "service_type_configuration": "ALL_V4",
    "comment": "test member",
    "is_master": True,
    "uuid": "mbr-uuid",
}


async def test_member_list() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response({"result": [_MBR_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member.list().all()
        assert results[0].host_name == "m1.example.com"
        assert "host_name" in captured[0].url.params["_return_fields+"]


async def test_member_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MBR_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member.get(_MBR_REF)
        assert obj.platform == "VNIOS"


async def test_member_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MBR_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member.find_one(host_name="m1.example.com")
        assert obj is not None


async def test_member_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MBR_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member.create({"host_name": "m1.example.com"})
        assert obj.host_name == "m1.example.com"
        assert captured[0].method == "POST"


async def test_member_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MBR_OBJ)

    async with _client(handler) as c:
        obj = Member(
            host_name="m1.example.com",
            comment="updated",
            is_master=True,
            uuid="mbr-uuid",
        )
        await c.grid.member.update(_MBR_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "is_master" not in body
        assert "uuid" not in body
        assert body.get("comment") == "updated"


async def test_member_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MBR_REF)

    async with _client(handler) as c:
        result = await c.grid.member.delete(_MBR_REF)
        assert _MBR_REF in result or result == _MBR_REF


async def test_member_restart_services() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response({})

    async with _client(handler) as c:
        await c.grid.member.restart_services(
            _MBR_REF, services=["DNS", "DHCP"], restart_option="FORCE_RESTART"
        )
        assert captured[0].method == "POST"
        assert "_function=restartservices" in str(captured[0].url)
        body = json.loads(captured[0].content.decode())
        assert body["services"] == ["DNS", "DHCP"]
        assert body["restart_option"] == "FORCE_RESTART"


# ============================================================= MemberDhcpproperties =====
_MDHCP_REF = "member:dhcpproperties/ZG5z:m1.example.com"
_MDHCP_OBJ = {
    "_ref": _MDHCP_REF,
    "host_name": "m1.example.com",
    "ipv4addr": "10.0.0.1",
    "authority": True,
}


async def test_member_dhcpproperties_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MDHCP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_dhcpproperties.list().all()
        assert results[0].authority is True


async def test_member_dhcpproperties_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MDHCP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_dhcpproperties.get(_MDHCP_REF)
        assert obj.ipv4addr == "10.0.0.1"


async def test_member_dhcpproperties_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MDHCP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_dhcpproperties.find_one()
        assert obj is not None


async def test_member_dhcpproperties_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MDHCP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_dhcpproperties.create({"authority": True})
        assert obj.authority is True
        assert captured[0].method == "POST"


async def test_member_dhcpproperties_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MDHCP_OBJ)

    async with _client(handler) as c:
        obj = MemberDhcpproperties(authority=True, host_name="m1.example.com", ipv4addr="10.0.0.1")
        await c.grid.member_dhcpproperties.update(_MDHCP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "ipv4addr" not in body
        assert body.get("authority") is True


async def test_member_dhcpproperties_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MDHCP_REF)

    async with _client(handler) as c:
        result = await c.grid.member_dhcpproperties.delete(_MDHCP_REF)
        assert _MDHCP_REF in result or result == _MDHCP_REF


# ============================================================= MemberDns =====
_MDNS_REF = "member:dns/ZG5z:m1.example.com"
_MDNS_OBJ = {
    "_ref": _MDNS_REF,
    "host_name": "m1.example.com",
    "ipv4addr": "10.0.0.1",
    "dnssec_enabled": False,
}


async def test_member_dns_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MDNS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_dns.list().all()
        assert results[0].dnssec_enabled is False


async def test_member_dns_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MDNS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_dns.get(_MDNS_REF)
        assert obj.ipv4addr == "10.0.0.1"


async def test_member_dns_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MDNS_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_dns.find_one()
        assert obj is not None


async def test_member_dns_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MDNS_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_dns.create({"forward_only": True})
        assert obj.host_name == "m1.example.com"
        assert captured[0].method == "POST"


async def test_member_dns_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MDNS_OBJ)

    async with _client(handler) as c:
        obj = MemberDns(forward_only=True, host_name="m1.example.com", uuid="u1")
        await c.grid.member_dns.update(_MDNS_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "uuid" not in body
        assert body.get("forward_only") is True


async def test_member_dns_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MDNS_REF)

    async with _client(handler) as c:
        result = await c.grid.member_dns.delete(_MDNS_REF)
        assert _MDNS_REF in result or result == _MDNS_REF


# ============================================================= MemberFiledistribution =====
_MFD_REF = "member:filedistribution/ZG5z:m1.example.com"
_MFD_OBJ = {
    "_ref": _MFD_REF,
    "host_name": "m1.example.com",
    "comment": "file dist",
    "status": "WORKING",
    "enable_ftp": True,
}


async def test_member_filedistribution_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MFD_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_filedistribution.list().all()
        assert results[0].enable_ftp is True


async def test_member_filedistribution_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MFD_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_filedistribution.get(_MFD_REF)
        assert obj.status == "WORKING"


async def test_member_filedistribution_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MFD_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_filedistribution.find_one()
        assert obj is not None


async def test_member_filedistribution_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MFD_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_filedistribution.create({"enable_ftp": True})
        assert obj.enable_ftp is True
        assert captured[0].method == "POST"


async def test_member_filedistribution_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MFD_OBJ)

    async with _client(handler) as c:
        obj = MemberFiledistribution(
            enable_ftp=True, host_name="m1.example.com", comment="file dist", status="WORKING"
        )
        await c.grid.member_filedistribution.update(_MFD_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "comment" not in body
        assert "status" not in body
        assert body.get("enable_ftp") is True


async def test_member_filedistribution_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MFD_REF)

    async with _client(handler) as c:
        result = await c.grid.member_filedistribution.delete(_MFD_REF)
        assert _MFD_REF in result or result == _MFD_REF


# ============================================================= MemberLicense =====
_ML_REF = "member:license/ZG5z:m1.example.com"
_ML_OBJ = {
    "_ref": _ML_REF,
    "hwid": "hw-001",
    "key": "abc123",
    "kind": "PERMANENT",
    "type": "NIOS",
    "uuid": "ml-uuid",
}


async def test_member_license_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_ML_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_license.list().all()
        assert results[0].hwid == "hw-001"


async def test_member_license_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_ML_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_license.get(_ML_REF)
        assert obj.type_ == "NIOS"


async def test_member_license_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_ML_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_license.find_one()
        assert obj is not None


async def test_member_license_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_ML_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_license.create({})
        assert obj.kind == "PERMANENT"
        assert captured[0].method == "POST"


async def test_member_license_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_ML_OBJ)

    async with _client(handler) as c:
        obj = MemberLicense(
            hwid="hw-001", key="abc123", kind="PERMANENT", type_="NIOS", uuid="ml-uuid"
        )
        await c.grid.member_license.update(_ML_REF, obj)
        body = json.loads(captured[0].content.decode())
        # all fields are readonly
        assert "hwid" not in body
        assert "key" not in body
        assert "uuid" not in body


async def test_member_license_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_ML_REF)

    async with _client(handler) as c:
        result = await c.grid.member_license.delete(_ML_REF)
        assert _ML_REF in result or result == _ML_REF


# ============================================================= MemberThreatprotection =====
_MTP_REF = "member:threatprotection/ZG5z:m1.example.com"
_MTP_OBJ = {
    "_ref": _MTP_REF,
    "host_name": "m1.example.com",
    "comment": "ATP",
    "enable_service": True,
}


async def test_member_threatprotection_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MTP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_threatprotection.list().all()
        assert results[0].enable_service is True


async def test_member_threatprotection_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MTP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_threatprotection.get(_MTP_REF)
        assert obj.host_name == "m1.example.com"


async def test_member_threatprotection_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MTP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_threatprotection.find_one()
        assert obj is not None


async def test_member_threatprotection_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MTP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_threatprotection.create({"enable_service": True})
        assert obj.enable_service is True
        assert captured[0].method == "POST"


async def test_member_threatprotection_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MTP_OBJ)

    async with _client(handler) as c:
        obj = MemberThreatprotection(
            enable_service=True, host_name="m1.example.com", comment="ATP"
        )
        await c.grid.member_threatprotection.update(_MTP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "comment" not in body
        assert body.get("enable_service") is True


async def test_member_threatprotection_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MTP_REF)

    async with _client(handler) as c:
        result = await c.grid.member_threatprotection.delete(_MTP_REF)
        assert _MTP_REF in result or result == _MTP_REF


# ============================================================= MemberParentalcontrol =====
_MPC_REF = "member:parentalcontrol/ZG5z:m1.example.com"
_MPC_OBJ = {"_ref": _MPC_REF, "name": "m1.example.com", "enable_service": True, "uuid": "mpc-uuid"}


async def test_member_parentalcontrol_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MPC_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_parentalcontrol.list().all()
        assert results[0].enable_service is True


async def test_member_parentalcontrol_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MPC_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_parentalcontrol.get(_MPC_REF)
        assert obj.name == "m1.example.com"


async def test_member_parentalcontrol_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MPC_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_parentalcontrol.find_one()
        assert obj is not None


async def test_member_parentalcontrol_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MPC_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_parentalcontrol.create({"enable_service": True})
        assert obj.enable_service is True
        assert captured[0].method == "POST"


async def test_member_parentalcontrol_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MPC_OBJ)

    async with _client(handler) as c:
        obj = MemberParentalcontrol(enable_service=True, name="m1.example.com", uuid="mpc-uuid")
        await c.grid.member_parentalcontrol.update(_MPC_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "name" not in body
        assert "uuid" not in body
        assert body.get("enable_service") is True


async def test_member_parentalcontrol_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MPC_REF)

    async with _client(handler) as c:
        result = await c.grid.member_parentalcontrol.delete(_MPC_REF)
        assert _MPC_REF in result or result == _MPC_REF


# ============================================================= MemberThreatinsight =====
_MTI_REF = "member:threatinsight/ZG5z:m1.example.com"
_MTI_OBJ = {
    "_ref": _MTI_REF,
    "host_name": "m1.example.com",
    "comment": "TI",
    "enable_service": True,
    "status": "WORKING",
}


async def test_member_threatinsight_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MTI_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.member_threatinsight.list().all()
        assert results[0].enable_service is True


async def test_member_threatinsight_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MTI_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_threatinsight.get(_MTI_REF)
        assert obj.status == "WORKING"


async def test_member_threatinsight_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MTI_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.member_threatinsight.find_one()
        assert obj is not None


async def test_member_threatinsight_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MTI_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.member_threatinsight.create({"enable_service": True})
        assert obj.enable_service is True
        assert captured[0].method == "POST"


async def test_member_threatinsight_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MTI_OBJ)

    async with _client(handler) as c:
        obj = MemberThreatinsight(
            enable_service=True, host_name="m1.example.com", comment="TI", status="WORKING"
        )
        await c.grid.member_threatinsight.update(_MTI_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "comment" not in body
        assert "status" not in body
        assert body.get("enable_service") is True


async def test_member_threatinsight_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MTI_REF)

    async with _client(handler) as c:
        result = await c.grid.member_threatinsight.delete(_MTI_REF)
        assert _MTI_REF in result or result == _MTI_REF


# ============================================================= Memberdfp =====
_MDFP_REF = "memberdfp/ZG5z:m1.example.com"
_MDFP_OBJ = {
    "_ref": _MDFP_REF,
    "host_name": "m1.example.com",
    "dfp_forward_first": True,
    "is_dfp_override": False,
    "uuid": "mdfp-uuid",
}


async def test_memberdfp_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MDFP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.memberdfp.list().all()
        assert results[0].dfp_forward_first is True


async def test_memberdfp_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MDFP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.memberdfp.get(_MDFP_REF)
        assert obj.host_name == "m1.example.com"


async def test_memberdfp_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_MDFP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.memberdfp.find_one()
        assert obj is not None


async def test_memberdfp_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MDFP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.memberdfp.create({"dfp_forward_first": True})
        assert obj.dfp_forward_first is True
        assert captured[0].method == "POST"


async def test_memberdfp_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_MDFP_OBJ)

    async with _client(handler) as c:
        obj = Memberdfp(dfp_forward_first=True, host_name="m1.example.com", uuid="mdfp-uuid")
        await c.grid.memberdfp.update(_MDFP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "host_name" not in body
        assert "uuid" not in body
        assert body.get("dfp_forward_first") is True


async def test_memberdfp_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_MDFP_REF)

    async with _client(handler) as c:
        result = await c.grid.memberdfp.delete(_MDFP_REF)
        assert _MDFP_REF in result or result == _MDFP_REF
