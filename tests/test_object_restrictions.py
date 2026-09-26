# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""The restriction gate: operations NIOS forbids must fail before any request.

``tests/fixtures/wapi_schema_v2.14.json`` records each object type's
``restrictions`` list as reported by ``?_schema``; a live grid answers a
restricted call with ``AdmConProtoError: Operation <op> not allowed for <type>``.
:mod:`ibx_nios_sdk._restrictions` mirrors that list so the SDK raises
``UnsupportedOperationError`` locally instead. These tests check the table
against the snapshot and the gate against a transport that fails on contact.

Regenerate the table with ``tools/refresh_object_restrictions.py``.
"""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from ibx_nios_sdk import NiosClient, UnsupportedOperationError
from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk._restrictions import OPERATIONS, RESTRICTED_OPS, restricted_ops
from tests.conftest import json_response
from tests.wapi_schema import ResourceInfo, iter_resources, load_snapshot

RESOURCES = [r for r in iter_resources() if r.wapi_type in load_snapshot()["objects"]]
RESTRICTED = [r for r in RESOURCES if restricted_ops(r.wapi_type)]
REF_SUFFIX = "ZG5z:test"


def _ids(res: ResourceInfo) -> str:
    return res.wapi_type


def _is_session_traffic(request: httpx.Request) -> bool:
    """True for the lazy Basic-auth login and the ``/logout`` on client close."""
    return request.headers.get("Authorization", "").startswith(
        "Basic "
    ) or request.url.path.endswith("/logout")


def _snapshot_restrictions(wapi_type: str) -> frozenset[str]:
    entry: dict[str, Any] = load_snapshot()["objects"][wapi_type]
    return frozenset(OPERATIONS & set(entry.get("restrictions", [])))


def _no_contact_client(*, enforce: bool = True) -> NiosClient:
    """A client whose transport fails the test if the SDK sends a WAPI request."""

    def handler(request: httpx.Request) -> httpx.Response:
        if _is_session_traffic(request):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        raise AssertionError(
            f"restricted operation reached the grid: {request.method} {request.url}"
        )

    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        enforce_restrictions=enforce,
        _transport=httpx.MockTransport(handler),
    )


async def _attempt(resource: WapiResource[Any], operation: str, wapi_type: str) -> None:
    """Invoke ``operation`` on ``resource`` the way a caller would."""
    ref = f"{wapi_type}/{REF_SUFFIX}"
    if operation == "read":
        await resource.list().all()
    elif operation == "create":
        await resource.create({"comment": "x"})
    elif operation == "update":
        await resource.update(ref, {"comment": "x"})
    else:
        await resource.delete(ref)


def test_table_matches_snapshot_restrictions() -> None:
    """Every entry in the generated table must match the grid's own schema."""
    expected = {
        r.wapi_type: _snapshot_restrictions(r.wapi_type)
        for r in RESOURCES
        if _snapshot_restrictions(r.wapi_type)
    }
    assert expected == RESTRICTED_OPS


def test_table_only_names_sdk_resource_types() -> None:
    assert not set(RESTRICTED_OPS) - {r.wapi_type for r in iter_resources()}


def test_table_only_names_known_operations() -> None:
    assert not {op for ops in RESTRICTED_OPS.values() for op in ops} - OPERATIONS


@pytest.mark.parametrize("res", RESTRICTED, ids=_ids)
async def test_restricted_operations_raise_without_a_request(res: ResourceInfo) -> None:
    """Each restricted operation raises UnsupportedOperationError, naming type and op."""
    async with _no_contact_client() as client:
        resource = res.resource(client._http)
        for operation in sorted(restricted_ops(res.wapi_type)):
            with pytest.raises(UnsupportedOperationError) as excinfo:
                await _attempt(resource, operation, res.wapi_type)
            assert excinfo.value.wapi_type == res.wapi_type
            assert excinfo.value.operation == operation
            assert res.wapi_type in str(excinfo.value)


@pytest.mark.parametrize("res", RESTRICTED, ids=_ids)
async def test_unrestricted_operations_still_reach_the_grid(res: ResourceInfo) -> None:
    """A partially restricted type keeps its allowed operations."""
    allowed = sorted(OPERATIONS - restricted_ops(res.wapi_type))
    if not allowed:
        pytest.skip("fully restricted object type")
    reached: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if _is_session_traffic(request):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        reached.append(request.method)
        if request.method == "DELETE":
            return json_response({"_value": f"{res.wapi_type}/{REF_SUFFIX}"})
        if request.method == "GET":
            return json_response({"result": [], "next_page_id": ""})
        return json_response({"result": {"_ref": f"{res.wapi_type}/{REF_SUFFIX}"}})

    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )
    async with client:
        resource = res.resource(client._http)
        for operation in allowed:
            await _attempt(resource, operation, res.wapi_type)
    assert len(reached) == len(allowed)


async def test_list_gate_fires_on_the_call_not_the_first_iteration() -> None:
    """``list()`` is not a coroutine, so it must check before returning the iterator."""
    async with _no_contact_client() as client:
        with pytest.raises(UnsupportedOperationError):
            client.dtc.dtc.list()


async def test_find_one_is_gated_through_list_page() -> None:
    async with _no_contact_client() as client:
        with pytest.raises(UnsupportedOperationError):
            await client.discovery.discovery.find_one()


async def test_set_extattrs_is_gated_through_update() -> None:
    async with _no_contact_client() as client:
        with pytest.raises(UnsupportedOperationError):
            await client.dns.allrecords.set_extattrs(f"allrecords/{REF_SUFFIX}", Site="NYC")


async def test_call_function_is_never_gated() -> None:
    """Function-only types restrict every operation but still accept function calls."""
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if _is_session_traffic(request):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        calls.append(request)
        return json_response({"status": "ok"})

    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )
    async with client:
        assert restricted_ops("dtc") == OPERATIONS
        result = await client.dtc.dtc.call_function(None, "add_certificate")
    assert result == {"status": "ok"}
    assert calls[0].url.params["_function"] == "add_certificate"


async def test_enforce_restrictions_false_sends_the_request() -> None:
    """Opt-out lets the grid answer, for versions whose restrictions differ."""
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if _is_session_traffic(request):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        requests.append(request)
        return json_response({"result": {"_ref": f"allrecords/{REF_SUFFIX}"}})

    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )
    async with client:
        await client.dns.allrecords.create({"name": "x"})
    assert [r.method for r in requests] == ["POST"]


async def test_unrestricted_type_is_unaffected() -> None:
    """A normal object type carries no restrictions and no extra checks."""
    assert restricted_ops("record:a") == frozenset()
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if _is_session_traffic(request):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        requests.append(request)
        return json_response({"result": {"_ref": f"record:a/{REF_SUFFIX}", "name": "a.example"}})

    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )
    async with client:
        await client.dns.record_a.create({"name": "a.example", "ipv4addr": "1.2.3.4"})
    assert [r.method for r in requests] == ["POST"]


def test_subclass_may_override_the_table() -> None:
    """An explicit ``_restricted_ops`` on a subclass wins over the generated table."""
    base = next(r.resource for r in RESTRICTED if r.wapi_type == "allrecords")
    assert base._restricted_ops == restricted_ops("allrecords")

    class Loosened(base):  # type: ignore[valid-type,misc]
        _restricted_ops = frozenset()

    assert Loosened._restricted_ops == frozenset()
