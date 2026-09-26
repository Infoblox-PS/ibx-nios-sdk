# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Targeted tests for the final coverage gaps in _http, _resource, and client."""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk._exceptions import NiosConnectionError
from ibx_nios_sdk.client import _resolve_verify
from ibx_nios_sdk.dns.models.record_a import RecordA
from tests.conftest import json_response, make_http_client


async def test_session_login_non_401_error_wraps_as_connection_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom")

    client = make_http_client(handler, max_retries=0)
    try:
        with pytest.raises(NiosConnectionError, match="(?i)login failed"):
            await client.get("/record:a")
    finally:
        await client.aclose()


async def _result_wrapper_client(handler_body: dict[str, object]) -> NiosClient:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(handler_body)

    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_create_unwraps_result_wrapper() -> None:
    ref = "record:a/ZG5z:unwrap.example.com/default"
    async with await _result_wrapper_client(
        {"result": {"_ref": ref, "name": "unwrap.example.com", "ipv4addr": "10.0.0.1"}}
    ) as c:
        obj = await c.dns.record_a.create({"name": "unwrap.example.com", "ipv4addr": "10.0.0.1"})
        assert obj.ref == ref
        assert obj.name == "unwrap.example.com"


async def test_update_unwraps_result_wrapper() -> None:
    ref = "record:a/ZG5z:unwrap.example.com/default"
    async with await _result_wrapper_client(
        {"result": {"_ref": ref, "name": "unwrap.example.com"}}
    ) as c:
        out = await c.dns.record_a.update(ref, RecordA(**{"_ref": ref, "comment": "updated"}))
        assert out.ref == ref


def test_resolve_verify_ca_bundle_beats_env(tmp_path: Path) -> None:
    bundle = tmp_path / "fake-ca.pem"
    assert _resolve_verify(True, bundle, "false") == str(bundle)


def test_resolve_verify_ca_bundle_beats_explicit_false(tmp_path: Path) -> None:
    bundle = tmp_path / "fake-ca.pem"
    assert _resolve_verify(False, bundle, None) == str(bundle)


def test_resolve_verify_env_var_flips_default() -> None:
    assert _resolve_verify(True, None, "false") is False
    assert _resolve_verify(True, None, "0") is False
    assert _resolve_verify(True, None, "NO") is False


def test_resolve_verify_env_var_ignored_when_verify_explicit() -> None:
    assert _resolve_verify(False, None, "false") is False
    assert _resolve_verify("/etc/ssl/cert.pem", None, "false") == "/etc/ssl/cert.pem"


def test_resolve_verify_default_passthrough() -> None:
    assert _resolve_verify(True, None, None) is True
    assert _resolve_verify(True, None, "true") is True
