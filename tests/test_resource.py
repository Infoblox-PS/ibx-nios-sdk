# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/test_resource.py
"""WapiResource base behavior - list_page, list, find_one."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from pydantic import BaseModel, ConfigDict

from ibx_nios_sdk._resource import WapiResource
from tests.conftest import json_response, make_http_client


class FakeA(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")
    _ref: str = ""
    name: str | None = None
    ipv4addr: str | None = None
    view_: str | None = None


class RecordAResource(WapiResource[FakeA]):
    _wapi_type = "record:a"
    _model = FakeA
    _default_return_fields = ["name", "ipv4addr", "view"]


def _session_and_list_handler(pages: list[dict[str, Any]]):
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls.append(request)
        idx = int(request.url.params.get("_page_id", "0") or "0")
        return json_response(pages[idx])

    return handler, calls


async def test_list_page_sends_paging_params() -> None:
    handler, calls = _session_and_list_handler(
        [{"result": [{"name": "a.example.com"}], "next_page_id": ""}]
    )
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        rows, next_id = await resource.list_page(name="a.example.com")
        assert next_id is None
        assert rows[0].name == "a.example.com"
        params = calls[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["_max_results"] == "1000"
        assert params["_return_fields+"] == "name,ipv4addr,view"
        assert params["name"] == "a.example.com"
    finally:
        await client.aclose()


async def test_list_iterates_pages() -> None:
    pages = [
        {"result": [{"name": "a"}, {"name": "b"}], "next_page_id": "1"},
        {"result": [{"name": "c"}], "next_page_id": ""},
    ]
    handler, _ = _session_and_list_handler(pages)
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        names = [r.name async for r in resource.list()]
        assert names == ["a", "b", "c"]
    finally:
        await client.aclose()


async def test_find_one_returns_first_or_none() -> None:
    handler, _ = _session_and_list_handler([{"result": [{"name": "a"}], "next_page_id": ""}])
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        match = await resource.find_one(name="a")
        assert match is not None and match.name == "a"
    finally:
        await client.aclose()


async def test_find_one_no_match() -> None:
    handler, _ = _session_and_list_handler([{"result": [], "next_page_id": ""}])
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        assert await resource.find_one(name="missing") is None
    finally:
        await client.aclose()


async def test_list_filter_operator() -> None:
    handler, calls = _session_and_list_handler([{"result": [], "next_page_id": ""}])
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        _ = [r async for r in resource.list(name__like="host")]
        assert calls[0].url.params["name~"] == "host"
    finally:
        await client.aclose()


async def test_get_by_ref_uses_ref_path_and_return_fields() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": "record:a/ZG5z:host.example.com/default", "name": "host.example.com"}
        )

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/ZG5z:host.example.com/default"
        obj = await resource.get(ref)
        assert obj.name == "host.example.com"
        path = captured[0].url.path
        assert path.endswith(f"/{ref}")
        assert captured[0].url.params["_return_fields+"] == "name,ipv4addr,view"
    finally:
        await client.aclose()


async def test_get_rejects_mismatched_ref() -> None:
    client = make_http_client(lambda r: json_response({}))
    try:
        resource = RecordAResource(client)
        with pytest.raises(ValueError, match="does not match wapi_type"):
            await resource.get("record:aaaa/XYZ:host/default")
    finally:
        await client.aclose()


async def test_create_posts_payload_and_returns_object() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": "record:a/NEW:host/default", "name": "host", "ipv4addr": "1.2.3.4"}
        )

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        payload = FakeA(name="host", ipv4addr="1.2.3.4")
        created = await resource.create(payload)
        assert created.name == "host"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params["_return_as_object"] == "1"
        body = httpx.Request("POST", req.url, content=req.content).content.decode()
        assert '"name":"host"' in body
        assert '"ipv4addr":"1.2.3.4"' in body
        # None fields excluded
        assert '"view"' not in body
    finally:
        await client.aclose()


async def test_update_puts_partial_payload() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {"_ref": request.url.path.split("/wapi/v2.14")[-1].lstrip("/"), "name": "host"}
        )

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        updated = await resource.update(ref, {"comment": "new comment"})
        assert updated.name == "host"
        req = captured[0]
        assert req.method == "PUT"
        assert req.url.path.endswith(f"/{ref}")
    finally:
        await client.aclose()


async def test_delete_returns_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("record:a/XYZ:host/default")

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        result = await resource.delete(ref)
        assert result == ref
    finally:
        await client.aclose()


async def test_call_function_on_ref() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ips": ["10.0.0.1", "10.0.0.2"]})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        result = await resource.call_function(ref, "next_available_ip", num=2)
        assert result == {"ips": ["10.0.0.1", "10.0.0.2"]}
        req = captured[0]
        assert req.method == "POST"
        assert req.url.path.endswith(f"/{ref}")
        assert req.url.params["_function"] == "next_available_ip"
        assert b'"num":2' in req.content
    finally:
        await client.aclose()


async def test_call_function_without_ref() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"ok": True})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        result = await resource.call_function(None, "global_helper", foo="bar")
        assert result == {"ok": True}
        req = captured[0]
        assert req.url.path.endswith("/record:a")
        assert req.url.params["_function"] == "global_helper"
    finally:
        await client.aclose()


async def test_list_page_with_explicit_page_id_sends_page_id_param() -> None:
    """Passing page_id to list_page must include _page_id in query params (line 128)."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"result": [], "next_page_id": ""})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        rows, next_id = await resource.list_page(page_id="abc123")
        assert next_id is None
        assert captured[0].url.params["_page_id"] == "abc123"
    finally:
        await client.aclose()


async def test_delete_returns_input_ref_when_no_value_in_response() -> None:
    """delete() must fall back to returning the input ref when body has no _value (line 401)."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        # Return a dict without _value - simulates an unexpected response shape
        return json_response({"some_other_key": "something"})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        result = await resource.delete(ref)
        assert result == ref
    finally:
        await client.aclose()


async def test_set_extattrs_updates_extattrs_field() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "record:a/XYZ:host/default", "name": "host"})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        await resource.set_extattrs(ref, Site="NYC", Owner="net-eng")
        req = captured[0]
        assert req.method == "PUT"
        body = req.content.decode()
        assert '"extattrs"' in body
        assert '"Site"' in body and '"NYC"' in body
        assert '"Owner"' in body and '"net-eng"' in body
    finally:
        await client.aclose()
