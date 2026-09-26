# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SecurityService scaffold tests - wiring and lazy property instantiation."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient, SecurityService
from ibx_nios_sdk.security._service import SecurityService as SecurityServiceDirect
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


async def test_security_service_accessible_on_client() -> None:
    """client.security should return a SecurityService instance."""
    c = _client()
    assert isinstance(c.security, SecurityService)


async def test_security_service_is_cached() -> None:
    """client.security should return the same object on repeated access."""
    c = _client()
    svc1 = c.security
    svc2 = c.security
    assert svc1 is svc2


async def test_security_service_imported_from_top_level() -> None:
    """SecurityService must be importable from ibx_nios_sdk top-level."""
    assert SecurityService is SecurityServiceDirect
