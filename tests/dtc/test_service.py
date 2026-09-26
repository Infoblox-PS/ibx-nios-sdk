# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcService scaffold tests - wiring and lazy property instantiation."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import DtcService, NiosClient
from ibx_nios_sdk.dtc._service import DtcService as DtcServiceDirect
from tests.conftest import json_response


def _client() -> NiosClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({})

    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_dtc_service_accessible_on_client() -> None:
    """client.dtc should return a DtcService instance."""
    c = _client()
    assert isinstance(c.dtc, DtcService)


async def test_dtc_service_is_cached() -> None:
    """client.dtc should return the same object on repeated access."""
    c = _client()
    svc1 = c.dtc
    svc2 = c.dtc
    assert svc1 is svc2


async def test_dtc_service_imported_from_top_level() -> None:
    """DtcService must be importable from ibx_nios_sdk top-level."""
    assert DtcService is DtcServiceDirect
