# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/test_client.py
"""NiosClient entry point and env-var configuration."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk._exceptions import NiosError
from tests.conftest import json_response


async def test_nios_client_is_async_context_manager() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        if request.url.path.endswith("/logout"):
            return json_response({})
        return json_response({})

    transport = httpx.MockTransport(handler)

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="admin",
        password="infoblox",
        _transport=transport,
    ) as client:
        assert client.grid_url == "https://grid.example.com"


async def test_env_vars_populate_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NIOS_GRID_URL", "https://env-grid.example.com")
    monkeypatch.setenv("NIOS_USERNAME", "envadmin")
    monkeypatch.setenv("NIOS_PASSWORD", "envpass")
    monkeypatch.setenv("NIOS_WAPI_VERSION", "2.12")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(_transport=transport)
    try:
        assert client.grid_url == "https://env-grid.example.com"
        assert client._http._wapi_version == "2.12"
        assert client._http._username == "envadmin"
    finally:
        await client.aclose()


async def test_missing_credentials_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("NIOS_USERNAME", "NIOS_PASSWORD"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(NiosError, match="credentials"):
        NiosClient(grid_url="https://g.example.com")


async def test_missing_grid_url_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """NiosClient without grid_url raises NiosError (line 112)."""
    monkeypatch.delenv("NIOS_GRID_URL", raising=False)
    with pytest.raises(NiosError, match="grid_url is required"):
        NiosClient(username="admin", password="secret")


async def test_ca_bundle_overrides_verify(tmp_path: pytest.TempPathFactory) -> None:
    """Passing ca_bundle must convert it to a string path and override verify (line 119)."""
    import pathlib

    # Create a minimal self-signed CA bundle file so httpx can parse it.
    # We just need a valid PEM placeholder (empty file causes an error, so use
    # the standard macOS system CA bundle if available, else create a blank cert
    # placeholder that httpx accepts without a real TLS connection happening).
    import tempfile

    ca_file = pathlib.Path(tempfile.mktemp(suffix=".pem"))
    # Write a minimal valid PEM header so ssl.create_default_context accepts it.
    # An empty cert store is fine; we never actually connect over TLS in this test.
    ca_file.write_text("")  # httpx may accept an empty file on some platforms

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({"ok": True})

    transport = httpx.MockTransport(handler)
    try:
        client = NiosClient(
            grid_url="https://g.example.com",
            username="admin",
            password="x",
            ca_bundle=str(ca_file),
            _transport=transport,
        )
        assert client.grid_url == "https://g.example.com"
        await client.aclose()
    finally:
        ca_file.unlink(missing_ok=True)


async def test_nios_client_dns_service() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    from ibx_nios_sdk.dns import DnsService

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )
    try:
        assert isinstance(client.dns, DnsService)
    finally:
        await client.aclose()


async def test_read_raw_uses_authenticated_wapi_transport() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.params.get("_schema") == "1":
            return httpx.Response(
                200,
                json={},
                headers={"Set-Cookie": "ibapauth=session-cookie; Path=/"},
            )
        return httpx.Response(
            200,
            json={"result": [{"network": "10.0.0.0/24", "comment": "lab"}]},
        )

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        _transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.read_raw(
            "network",
            params={"_return_fields": "network,comment"},
        )

    raw_request = next(request for request in requests if request.url.path.endswith("/network"))
    assert raw_request.method == "GET"
    assert raw_request.url.path == "/wapi/v2.14/network"
    assert dict(raw_request.url.params) == {"_return_fields": "network,comment"}
    assert raw_request.headers["cookie"] == "ibapauth=session-cookie"
    assert result == {"result": [{"network": "10.0.0.0/24", "comment": "lab"}]}


async def test_read_raw_preserves_top_level_json_arrays() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{"name": "default"}])

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        _transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.read_raw("networkview")

    assert result == [{"name": "default"}]


async def test_read_raw_reuses_retry_aware_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    attempts = 0

    async def no_sleep(_delay: float) -> None:
        return None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(503, json={"Error": "temporarily unavailable"})
        return httpx.Response(200, json={"result": [{"name": "default"}]})

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", no_sleep)
    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        max_retries=1,
        _transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.read_raw("networkview")

    assert attempts == 2
    assert result == {"result": [{"name": "default"}]}


@pytest.mark.parametrize(
    "object_type",
    [
        "",
        "/",
        "/network",
        "//attacker.example/network",
        "https://attacker.example/network",
        "network/one",
        "network//one",
        "network\\one",
        "network?password=secret",
        "network#fragment",
        "network\nmember",
        ".",
        "..",
        "%2e%2e",
        "%252e%252e",
        "network%2f..%2fgrid",
        "network%252f..%252fgrid",
        "Network",
    ],
)
async def test_read_raw_rejects_unsafe_wapi_object_paths(object_type: str) -> None:
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        return httpx.Response(200, json={})

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        _transport=httpx.MockTransport(handler),
    ) as client:
        with pytest.raises(ValueError, match="WAPI object"):
            await client.read_raw(object_type)

    assert request_count == 0


@pytest.mark.parametrize(
    "parameter_name",
    [
        "api_key",
        "API-KEY",
        "ApiKey",
        "password",
        "PassWord",
        "token",
        "ToKeN",
        "access_token",
        "Authorization",
        "client-secret",
    ],
)
async def test_read_raw_rejects_secret_bearing_parameter_names(parameter_name: str) -> None:
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        return httpx.Response(200, json={})

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        _transport=httpx.MockTransport(handler),
    ) as client:
        with pytest.raises(ValueError, match="secret-bearing"):
            await client.read_raw("record:a", params={parameter_name: "must-not-leak"})

    assert request_count == 0


@pytest.mark.parametrize(
    "params",
    [
        {"_max_results": 100},
        {b"_schema": "1"},
        {"_schema": None},
    ],
)
async def test_read_raw_rejects_non_string_parameters(params: dict) -> None:
    """Only string names and values reach the WAPI query string."""
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        return httpx.Response(200, json={})

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        _transport=httpx.MockTransport(handler),
    ) as client:
        with pytest.raises(ValueError, match="only string names and values"):
            await client.read_raw("record:a", params=params)

    assert request_count == 0


async def test_read_raw_accepts_schema_and_paging_parameters() -> None:
    seen_params: httpx.QueryParams | None = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_params
        seen_params = request.url.params
        return httpx.Response(200, json={"fields": []})

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        _transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.read_raw(
            "record:a",
            params={"_schema": "1", "_schema_type": "All", "_max_results": "100"},
        )

    assert seen_params is not None
    assert dict(seen_params) == {"_schema": "1", "_schema_type": "All", "_max_results": "100"}
    assert result == {"fields": []}


async def test_read_schema_reads_authenticated_wapi_root_schema() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={"supported_versions": ["2.12.3", "2.14"]},
            headers={"Set-Cookie": "ibapauth=session-cookie; Path=/"},
        )

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        _transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.read_schema()

    schema_request = requests[0]
    assert schema_request.method == "GET"
    assert schema_request.url.path == "/wapi/v2.14/"
    assert dict(schema_request.url.params) == {"_schema": "1"}
    assert schema_request.headers["authorization"].startswith("Basic ")
    assert result == {"supported_versions": ["2.12.3", "2.14"]}


async def test_read_schema_reads_object_schema_through_retry_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attempts = 0

    async def no_sleep(_delay: float) -> None:
        return None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return httpx.Response(503, json={"Error": "temporarily unavailable"})
        return httpx.Response(200, json={"fields": [{"name": "network", "supports": "r"}]})

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", no_sleep)
    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        max_retries=1,
        _transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.read_schema("network")

    assert attempts == 2
    assert result == {"fields": [{"name": "network", "supports": "r"}]}


@pytest.mark.parametrize("object_type", ["", "/network", "network?x=1", "Network"])
async def test_read_schema_rejects_unsafe_object_paths(object_type: str) -> None:
    request_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal request_count
        request_count += 1
        return httpx.Response(200, json={})

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="reader",
        password="secret",
        use_session=False,
        _transport=httpx.MockTransport(handler),
    ) as client:
        with pytest.raises(ValueError, match="WAPI object"):
            await client.read_schema(object_type)

    assert request_count == 0
