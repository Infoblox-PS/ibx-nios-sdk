# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/_http/test_edge_cases.py
"""Edge-case coverage for _http.py helpers and HttpClient paths."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import AuthenticationError, NiosConnectionError
from ibx_nios_sdk._http import (
    _extract_error_message,
    _parse_retry_after,
    _safe_json,
)
from tests.conftest import json_response, make_http_client

# ---------------------------------------------------------------------------
# _parse_retry_after - ValueError branch (non-numeric header value)
# ---------------------------------------------------------------------------


def test_parse_retry_after_non_numeric_returns_none() -> None:
    """_parse_retry_after must return None when the header is not a number."""
    response = httpx.Response(
        429,
        content=b"{}",
        headers={"Retry-After": "Wed, 21 Oct 2025 07:28:00 GMT"},
    )
    result = _parse_retry_after(response)
    assert result is None


# ---------------------------------------------------------------------------
# _safe_json - Exception branch (invalid JSON body)
# ---------------------------------------------------------------------------


def test_safe_json_invalid_body_returns_none() -> None:
    """_safe_json must return None when the response body is not valid JSON."""
    response = httpx.Response(200, content=b"not-json-at-all")
    result = _safe_json(response)
    assert result is None


def test_safe_json_non_dict_json_wrapped() -> None:
    """_safe_json wraps non-dict JSON (array) in {'_value': ...}."""
    import json

    response = httpx.Response(
        200,
        content=json.dumps([1, 2, 3]).encode(),
        headers={"Content-Type": "application/json"},
    )
    result = _safe_json(response)
    assert result == {"_value": [1, 2, 3]}


# ---------------------------------------------------------------------------
# _extract_error_message - body-is-not-a-dict branch (line 549)
#                        - body has no Error/text string (line 554)
# ---------------------------------------------------------------------------


def test_extract_error_message_non_dict_returns_none() -> None:
    """_extract_error_message returns None when body is not a dict."""
    assert _extract_error_message(None) is None


def test_extract_error_message_no_error_key_returns_none() -> None:
    """_extract_error_message returns None when neither 'Error' nor 'text' is a string."""
    assert _extract_error_message({"code": 123}) is None


# ---------------------------------------------------------------------------
# HttpClient._login - 401 response raises AuthenticationError (line 187)
# ---------------------------------------------------------------------------


async def test_login_401_raises_authentication_error() -> None:
    """A 401 from /grid/session during login must raise AuthenticationError."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return json_response(
                {
                    "Error": "AdmConProtoError: Invalid username or password",
                    "code": "Client.Ibap.Proto",
                },
                status_code=401,
            )
        return json_response({})

    client = make_http_client(handler)
    try:
        with pytest.raises(AuthenticationError):
            await client.request("GET", "/grid")
    finally:
        await client._client.aclose()


# ---------------------------------------------------------------------------
# HttpClient._logout - exception silenced (lines 204-205)
# ---------------------------------------------------------------------------


async def test_logout_exception_is_silenced() -> None:
    """Errors raised during _logout must be swallowed so aclose() always completes."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        if request.url.path.endswith("/logout"):
            raise httpx.ConnectError("network gone during logout")
        return json_response({})

    client = make_http_client(handler)
    # Trigger login so _logged_in=True
    await client.request("GET", "/grid")
    # aclose must not raise even though _logout will encounter a ConnectError
    await client.aclose()  # no assertion needed - must not raise


# ---------------------------------------------------------------------------
# HttpClient.get_with_return_fields - extra_params branch (line 386)
# ---------------------------------------------------------------------------


async def test_get_with_return_fields_extra_params_merged() -> None:
    """extra_params must be merged into the query string."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name"],
            extra_params={"_return_as_object": "1"},
        )
        req = captured[0]
        assert req.url.params["_return_as_object"] == "1"
        assert "_return_fields+" in req.url.params
    finally:
        await client.aclose()


# ---------------------------------------------------------------------------
# HttpClient._send - TLS ConnectError path (lines 465-475)
# ---------------------------------------------------------------------------


async def test_send_tls_error_raises_nios_connection_error() -> None:
    """A TLS ConnectError during _send (not _login) must raise NiosConnectionError."""

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.headers.get("Authorization", "").startswith("Basic "):
            # Login succeeds
            return httpx.Response(
                200,
                json=[{}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        raise httpx.ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED] self signed certificate")

    client = make_http_client(handler)
    try:
        with pytest.raises(NiosConnectionError) as exc_info:
            await client.request("GET", "/grid")
        msg = exc_info.value.message
        assert "TLS verification failed" in msg
    finally:
        await client._client.aclose()


async def test_send_non_tls_connect_error_raises_nios_connection_error() -> None:
    """A non-TLS ConnectError during _send must raise NiosConnectionError."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        raise httpx.ConnectError("Connection refused")

    client = make_http_client(handler)
    try:
        with pytest.raises(NiosConnectionError) as exc_info:
            await client.request("GET", "/grid")
        assert "Connection failed" in exc_info.value.message
    finally:
        await client._client.aclose()


# ---------------------------------------------------------------------------
# HttpClient._handle_response - 204 No Content returns None (line 495)
# ---------------------------------------------------------------------------


async def test_handle_response_204_returns_none() -> None:
    """A 204 No Content response must result in None from request()."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        return httpx.Response(204)

    client = make_http_client(handler)
    try:
        result = await client.request("DELETE", "/record:a/XYZ")
        assert result is None
    finally:
        await client.aclose()
