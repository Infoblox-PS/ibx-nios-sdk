# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RequestResource - function-only /request endpoint."""

from __future__ import annotations

import json
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


async def test_request_submit_batch() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response([{"result": "ok"}, {"result": "ok2"}])

    body = [
        {"method": "GET", "object": "record:a", "data": {"name": "a.example.com"}},
        {"method": "GET", "object": "record:a", "data": {"name": "b.example.com"}},
    ]
    async with _client(handler) as c:
        result = await c.misc.request.submit(body)
        assert isinstance(result, list)
        assert result[0]["result"] == "ok"
        assert result[1]["result"] == "ok2"

        req = captured[0]
        assert req.method == "POST"
        assert "/request" in req.url.path
        assert json.loads(req.content.decode()) == body


async def test_request_submit_single() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": "ok"})

    body = {"method": "GET", "object": "record:a", "data": {"name": "a.example.com"}}
    async with _client(handler) as c:
        result = await c.misc.request.submit(body)
        assert result == {"result": "ok"}
        assert json.loads(captured[0].content.decode()) == body


async def test_request_none_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return httpx.Response(204)

    async with _client(handler) as c:
        result = await c.misc.request.submit([{"method": "GET", "object": "record:a"}])
        assert result == []
