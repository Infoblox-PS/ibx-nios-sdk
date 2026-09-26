# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SearchResource - function-only resource tests."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


def _make_handler(response_body: Any) -> Any:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(response_body)

    return handler, captured


async def test_search_search_issues_get_request() -> None:
    """search() should GET /search with query params.

    The WAPI /search endpoint returns a JSON array; the SDK HTTP layer wraps
    arrays as {"_value": [...]}, so the mock handler returns a dict with _value.
    """
    handler, captured = _make_handler(
        {"_value": [{"_ref": "record:a/abc", "name": "host.example.com"}]}
    )
    async with _client(handler) as c:
        results = await c.misc.search.search(search_string="host.example.com")
        req = captured[0]
        assert req.method == "GET"
        assert "/search" in req.url.path
        assert req.url.params.get("search_string") == "host.example.com"
        assert len(results) == 1
        assert results[0]["name"] == "host.example.com"


async def test_search_search_returns_empty_for_non_list() -> None:
    """search() should return [] if response is not a list."""
    handler, captured = _make_handler({"something": "else"})
    async with _client(handler) as c:
        results = await c.misc.search.search(search_string="nothing")
        assert results == []


async def test_search_call_generic_dispatch() -> None:
    """call() should POST to /search?_function=<name>."""
    handler, captured = _make_handler({"result": "ok"})
    async with _client(handler) as c:
        result = await c.misc.search.call("somefunc", param="value")
        req = captured[0]
        assert req.method == "POST"
        assert "/search" in req.url.path
        assert req.url.params["_function"] == "somefunc"
        assert result == {"result": "ok"}


async def test_search_returns_empty_list_when_response_is_none() -> None:
    """search() returns [] when the server returns 204 No Content (data is None)."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return httpx.Response(204)

    async with _client(handler) as c:
        results = await c.misc.search.search(search_string="nothing")
        assert results == []
