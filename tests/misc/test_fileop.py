# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FileopResource - function-only resource tests."""

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


async def test_fileop_upload_init_posts_correct_function() -> None:
    """upload_init() should POST to /fileop?_function=uploadinit."""
    handler, captured = _make_handler({"token": "abc123", "url": "https://upload.example.com"})
    async with _client(handler) as c:
        result = await c.misc.fileop.upload_init()
        req = captured[0]
        assert req.method == "POST"
        assert "/fileop" in req.url.path
        assert req.url.params["_function"] == "uploadinit"
        assert result["token"] == "abc123"


async def test_fileop_csv_import_posts_correct_function() -> None:
    """csv_import() should POST to /fileop?_function=csv_import."""
    handler, captured = _make_handler({"token": "import-token"})
    async with _client(handler) as c:
        result = await c.misc.fileop.csv_import(token="upload-token", action="MERGE")
        req = captured[0]
        assert req.url.params["_function"] == "csv_import"
        assert req.method == "POST"
        assert result == {"token": "import-token"}


async def test_fileop_csv_export_posts_correct_function() -> None:
    """csv_export() should POST to /fileop?_function=csv_export."""
    handler, captured = _make_handler({"token": "export-token", "url": "https://dl.example.com"})
    async with _client(handler) as c:
        result = await c.misc.fileop.csv_export(_object_type="record:a")
        req = captured[0]
        assert req.url.params["_function"] == "csv_export"
        assert "export-token" in str(result)


async def test_fileop_download_complete_posts_correct_function() -> None:
    """download_complete() should POST to /fileop?_function=downloadcomplete."""
    handler, captured = _make_handler({})
    async with _client(handler) as c:
        await c.misc.fileop.download_complete(token="tok")
        req = captured[0]
        assert req.url.params["_function"] == "downloadcomplete"


async def test_fileop_upload_certificate_posts_correct_function() -> None:
    """upload_certificate() should POST to /fileop?_function=uploadcertificate."""
    handler, captured = _make_handler({})
    async with _client(handler) as c:
        await c.misc.fileop.upload_certificate(token="tok")
        req = captured[0]
        assert req.url.params["_function"] == "uploadcertificate"


async def test_fileop_call_generic_dispatch() -> None:
    """call() should dispatch to the named function."""
    handler, captured = _make_handler({"result": "ok"})
    async with _client(handler) as c:
        result = await c.misc.fileop.call("getgriddata", token="tok")
        req = captured[0]
        assert req.url.params["_function"] == "getgriddata"
        assert result == {"result": "ok"}


async def test_fileop_downloadcertificate_posts_correct_function() -> None:
    """downloadcertificate() should POST to /fileop?_function=downloadcertificate."""
    handler, captured = _make_handler({})
    async with _client(handler) as c:
        await c.misc.fileop.downloadcertificate(token="tok")
        req = captured[0]
        assert req.url.params["_function"] == "downloadcertificate"


async def test_fileop_csv_snapshot_file_posts_correct_function() -> None:
    """csv_snapshot_file() should POST to /fileop?_function=csv_snapshot_file."""
    handler, captured = _make_handler({})
    async with _client(handler) as c:
        await c.misc.fileop.csv_snapshot_file(token="tok")
        req = captured[0]
        assert req.url.params["_function"] == "csv_snapshot_file"
