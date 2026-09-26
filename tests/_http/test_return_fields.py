# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_return_fields.py
"""HttpClient integrates _return_fields via build_return_fields_params."""

from __future__ import annotations

import httpx

from tests.conftest import json_response, make_http_client


async def _session_handler(store: dict[str, httpx.Request]) -> None:
    """Helper: no-op - see individual tests."""


async def test_get_auto_adds_return_fields_plus() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name", "ipv4addr", "view"],
        )
        req = captured[0]
        assert req.url.params["_return_fields+"] == "name,ipv4addr,view"
    finally:
        await client.aclose()


async def test_get_with_explicit_return_fields() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name", "ipv4addr"],
            return_fields=["name"],
        )
        req = captured[0]
        assert req.url.params["_return_fields"] == "name"
        assert "_return_fields+" not in req.url.params
    finally:
        await client.aclose()


async def test_get_with_return_fields_plus_extends() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name", "ipv4addr"],
            return_fields_plus=["extattrs"],
        )
        req = captured[0]
        assert req.url.params["_return_fields+"] == "name,ipv4addr,extattrs"
    finally:
        await client.aclose()
