# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HostnamerewritepolicyResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.hostnamerewritepolicy import Hostnamerewritepolicy
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        # WAPI restricts some operations on this object type; the gate itself is
        # covered in tests/test_object_restrictions.py, so keep it off here and
        # exercise the generic WapiResource layer against the mock transport.
        enforce_restrictions=False,
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns hostnamerewritepolicy objects
# ---------------------------------------------------------------------------


async def test_hostnamerewritepolicy_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "hostnamerewritepolicy/ZG5z:default",
                        "name": "default",
                        "comment": "Default policy",
                        "pre_script": "",
                        "post_script": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        policies = await c.ipam.hostnamerewritepolicy.list().all()
        assert len(policies) == 1
        p = policies[0]
        assert p.name == "default"
        assert p.comment == "Default policy"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_hostnamerewritepolicy_list_by_name() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "hostnamerewritepolicy/ZG5z:default",
                        "name": "default",
                        "comment": "",
                        "pre_script": "",
                        "post_script": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        policies = await c.ipam.hostnamerewritepolicy.list(name="default").all()
        assert len(policies) == 1
        params = captured[0].url.params
        assert params.get("name") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_hostnamerewritepolicy_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "hostnamerewritepolicy/ZG5z:default",
                "name": "default",
                "comment": "Default policy",
                "pre_script": "trim",
                "post_script": "lowercase",
                "replacement_character": "-",
                "valid_characters": "a-z0-9",
            }
        )

    async with _client(handler) as c:
        ref = "hostnamerewritepolicy/ZG5z:default"
        p = await c.ipam.hostnamerewritepolicy.get(ref)
        assert p.name == "default"
        assert p.replacement_character == "-"
        assert p.valid_characters == "a-z0-9"


# ---------------------------------------------------------------------------
# 4. find_one(name="default") - returns first match
# ---------------------------------------------------------------------------


async def test_hostnamerewritepolicy_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "hostnamerewritepolicy/ZG5z:default",
                        "name": "default",
                        "comment": "",
                        "pre_script": "",
                        "post_script": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        p = await c.ipam.hostnamerewritepolicy.find_one(name="default")
        assert p is not None
        assert p.name == "default"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_hostnamerewritepolicy_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "hostnamerewritepolicy/ZG5z:custom",
                "name": "custom",
                "comment": "Custom policy",
                "pre_script": "",
                "post_script": "",
            }
        )

    async with _client(handler) as c:
        p = await c.ipam.hostnamerewritepolicy.create(
            {"name": "custom", "comment": "Custom policy", "replacement_character": "_"}
        )
        assert p.name == "custom"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"custom"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (is_default, pre_defined, uuid)
# ---------------------------------------------------------------------------


async def test_hostnamerewritepolicy_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "hostnamerewritepolicy/ZG5z:custom",
                "name": "custom",
                "comment": "updated",
                "pre_script": "",
                "post_script": "",
            }
        )

    async with _client(handler) as c:
        ref = "hostnamerewritepolicy/ZG5z:custom"
        policy = Hostnamerewritepolicy(
            name="custom",
            comment="updated",
            is_default=True,  # RO
            pre_defined=False,  # RO
            uuid="some-uuid",  # RO
        )
        await c.ipam.hostnamerewritepolicy.update(ref, policy)
        body = json.loads(captured[0].content.decode())

        assert "is_default" not in body, "is_default is readonly - must be stripped"
        assert "pre_defined" not in body, "pre_defined is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("comment") == "updated"
