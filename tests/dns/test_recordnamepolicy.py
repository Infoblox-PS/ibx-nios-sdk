# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordnamepolicyResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.recordnamepolicy import Recordnamepolicy
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list with filter
# ---------------------------------------------------------------------------


async def test_recordnamepolicy_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "recordnamepolicy/ZG5z:default",
                        "name": "default",
                        "is_default": True,
                        "regex": ".*",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        policies = await c.dns.recordnamepolicy.list().all()
        assert len(policies) == 1
        p = policies[0]
        assert p.name == "default"
        assert p.is_default is True
        assert p.regex == ".*"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get by ref
# ---------------------------------------------------------------------------


async def test_recordnamepolicy_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "recordnamepolicy/ZG5z:strict",
                "name": "strict",
                "is_default": False,
                "regex": r"^[a-z0-9\-]+$",
                "pre_defined": False,
            }
        )

    async with _client(handler) as c:
        ref = "recordnamepolicy/ZG5z:strict"
        p = await c.dns.recordnamepolicy.get(ref)
        assert p.name == "strict"
        assert p.is_default is False
        assert p.regex == r"^[a-z0-9\-]+$"
        assert p.pre_defined is False


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_recordnamepolicy_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "recordnamepolicy/ZG5z:default",
                        "name": "default",
                        "is_default": True,
                        "regex": ".*",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        p = await c.dns.recordnamepolicy.find_one(name="default")
        assert p is not None
        assert p.name == "default"
        assert p.is_default is True


# ---------------------------------------------------------------------------
# 4. create - POST body contains submitted fields
# ---------------------------------------------------------------------------


async def test_recordnamepolicy_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "recordnamepolicy/ZG5z:custom",
                "name": "custom",
                "is_default": False,
                "regex": r"^[a-z]+$",
            }
        )

    async with _client(handler) as c:
        p = await c.dns.recordnamepolicy.create(
            {"name": "custom", "is_default": False, "regex": r"^[a-z]+$"}
        )
        assert p.name == "custom"
        body = captured[0].content.decode()
        assert '"name":"custom"' in body
        assert '"is_default":false' in body


# ---------------------------------------------------------------------------
# 5. update strips readonly fields
# ---------------------------------------------------------------------------


async def test_recordnamepolicy_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "recordnamepolicy/ZG5z:custom",
                "name": "custom",
                "is_default": False,
                "regex": r"^updated$",
            }
        )

    async with _client(handler) as c:
        ref = "recordnamepolicy/ZG5z:custom"
        p = Recordnamepolicy(
            name="custom",
            is_default=False,
            regex=r"^updated$",
            pre_defined=True,  # RO
            uuid="some-uuid",  # RO
        )
        await c.dns.recordnamepolicy.update(ref, p)
        body = captured[0].content.decode()
        # Readonly fields must not appear
        assert '"pre_defined"' not in body, "pre_defined is readonly - must be stripped"
        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        # Writable fields must be present
        assert '"name":"custom"' in body
        assert '"regex"' in body


# ---------------------------------------------------------------------------
# 6. delete returns ref
# ---------------------------------------------------------------------------


async def test_recordnamepolicy_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("recordnamepolicy/ZG5z:custom")

    async with _client(handler) as c:
        result = await c.dns.recordnamepolicy.delete("recordnamepolicy/ZG5z:custom")
        assert result == "recordnamepolicy/ZG5z:custom"
