# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for licensing resources: GridLicensePool, GridLicensePoolContainer, LicenseGridwide, GridX509certificate."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.grid.models.grid_license_pool import GridLicensePool
from ibx_nios_sdk.grid.models.grid_license_pool_container import GridLicensePoolContainer
from ibx_nios_sdk.grid.models.grid_x509certificate import GridX509certificate
from ibx_nios_sdk.grid.models.license_gridwide import LicenseGridwide
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


# ============================================================= GridLicensePool =====
_LP_REF = "grid:license_pool/ZG5z:lp1"
_LP_OBJ = {
    "_ref": _LP_REF,
    "type": "NIOS",
    "key": "lp-key",
    "limit": "10",
    "installed": 10,
    "assigned": 2,
    "uuid": "lp-uuid",
}


async def test_grid_license_pool_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_LP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_license_pool.list().all()
        assert results[0].type == "NIOS"


async def test_grid_license_pool_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_LP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_license_pool.get(_LP_REF)
        assert obj.installed == 10


async def test_grid_license_pool_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_LP_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_license_pool.find_one()
        assert obj is not None


async def test_grid_license_pool_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_LP_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_license_pool.create({"key": "lp-key"})
        assert obj.key == "lp-key"
        assert captured[0].method == "POST"


async def test_grid_license_pool_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_LP_OBJ)

    async with _client(handler) as c:
        obj = GridLicensePool(type="NIOS", key="lp-key", limit="10", uuid="lp-uuid")
        await c.grid.grid_license_pool.update(_LP_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "type" not in body
        assert "uuid" not in body
        assert "key" not in body


async def test_grid_license_pool_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_LP_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_license_pool.delete(_LP_REF)
        assert _LP_REF in result or result == _LP_REF


# ============================================================= GridLicensePoolContainer =====
_LPC_REF = "grid:license_pool_container/ZG5z:lpc1"
_LPC_OBJ = {
    "_ref": _LPC_REF,
    "lpc_uid": "lpc-uid-1",
    "last_entitlement_update": 1700000000,
    "uuid": "lpc-uuid",
}


async def test_grid_license_pool_container_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_LPC_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_license_pool_container.list().all()
        assert results[0].lpc_uid == "lpc-uid-1"


async def test_grid_license_pool_container_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_LPC_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_license_pool_container.get(_LPC_REF)
        assert obj.lpc_uid == "lpc-uid-1"


async def test_grid_license_pool_container_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_LPC_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_license_pool_container.find_one()
        assert obj is not None


async def test_grid_license_pool_container_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_LPC_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_license_pool_container.create({"allocate_licenses": {}})
        assert obj.lpc_uid == "lpc-uid-1"
        assert captured[0].method == "POST"


async def test_grid_license_pool_container_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_LPC_OBJ)

    async with _client(handler) as c:
        obj = GridLicensePoolContainer(lpc_uid="lpc-uid-1", uuid="lpc-uuid", allocate_licenses={})
        await c.grid.grid_license_pool_container.update(_LPC_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "lpc_uid" not in body
        assert "uuid" not in body
        assert "allocate_licenses" in body


async def test_grid_license_pool_container_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_LPC_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_license_pool_container.delete(_LPC_REF)
        assert _LPC_REF in result or result == _LPC_REF


# ============================================================= LicenseGridwide =====
_LGW_REF = "license:gridwide/ZG5z:lgw1"
_LGW_OBJ = {
    "_ref": _LGW_REF,
    "type": "NIOS_ONE_PORT",
    "key": "lgw-key",
    "limit": "unlimited",
    "expiration_status": "VALID",
    "uuid": "lgw-uuid",
}


async def test_license_gridwide_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_LGW_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.license_gridwide.list().all()
        assert results[0].type_ == "NIOS_ONE_PORT"


async def test_license_gridwide_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_LGW_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.license_gridwide.get(_LGW_REF)
        assert obj.expiration_status == "VALID"


async def test_license_gridwide_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_LGW_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.license_gridwide.find_one()
        assert obj is not None


async def test_license_gridwide_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_LGW_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.license_gridwide.create({"key": "lgw-key"})
        assert obj.key == "lgw-key"
        assert captured[0].method == "POST"


async def test_license_gridwide_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_LGW_OBJ)

    async with _client(handler) as c:
        obj = LicenseGridwide(type="NIOS_ONE_PORT", key="lgw-key", uuid="lgw-uuid")
        await c.grid.license_gridwide.update(_LGW_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "type" not in body
        assert "uuid" not in body
        assert "key" not in body


async def test_license_gridwide_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_LGW_REF)

    async with _client(handler) as c:
        result = await c.grid.license_gridwide.delete(_LGW_REF)
        assert _LGW_REF in result or result == _LGW_REF


# ============================================================= GridX509certificate =====
_X509_REF = "grid:x509certificate/ZG5z:cert1"
_X509_OBJ = {
    "_ref": _X509_REF,
    "subject": "CN=infoblox.example.com",
    "issuer": "CN=CA",
    "serial": "ABCDEF01",
    "valid_not_before": 1700000000,
    "valid_not_after": 1800000000,
    "uuid": "cert-uuid",
}


async def test_grid_x509certificate_list() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_X509_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        results = await c.grid.grid_x509certificate.list().all()
        assert results[0].subject == "CN=infoblox.example.com"


async def test_grid_x509certificate_get() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_X509_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_x509certificate.get(_X509_REF)
        assert obj.issuer == "CN=CA"


async def test_grid_x509certificate_find_one() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"result": [_X509_OBJ], "next_page_id": ""})

    async with _client(handler) as c:
        obj = await c.grid.grid_x509certificate.find_one()
        assert obj is not None


async def test_grid_x509certificate_create() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_X509_OBJ)

    async with _client(handler) as c:
        obj = await c.grid.grid_x509certificate.create({"subject": "CN=infoblox.example.com"})
        assert obj.subject == "CN=infoblox.example.com"
        assert captured[0].method == "POST"


async def test_grid_x509certificate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(r)
        return json_response(_X509_OBJ)

    async with _client(handler) as c:
        obj = GridX509certificate(
            subject="CN=infoblox.example.com",
            issuer="CN=CA",
            serial="ABCDEF01",
            uuid="cert-uuid",
        )
        await c.grid.grid_x509certificate.update(_X509_REF, obj)
        body = json.loads(captured[0].content.decode())
        assert "subject" not in body
        assert "uuid" not in body


async def test_grid_x509certificate_delete() -> None:
    def handler(r: httpx.Request) -> httpx.Response:
        if r.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(_X509_REF)

    async with _client(handler) as c:
        result = await c.grid.grid_x509certificate.delete(_X509_REF)
        assert _X509_REF in result or result == _X509_REF
