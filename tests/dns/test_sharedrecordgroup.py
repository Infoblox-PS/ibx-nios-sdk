# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordgroupResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.sharedrecordgroup import Sharedrecordgroup
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(record_name_policy="Strict Hostname Checking")
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecordgroup/ZG5z:my-group",
                        "name": "my-group",
                        "record_name_policy": "Strict Hostname Checking",
                        "use_record_name_policy": True,
                        "comment": "shared group",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.sharedrecordgroup.list(
            record_name_policy="Strict Hostname Checking"
        ).all()
        assert len(groups) == 1
        g = groups[0]
        assert g.name == "my-group"
        assert g.record_name_policy == "Strict Hostname Checking"
        assert g.use_record_name_policy is True

        params = captured[0].url.params
        assert params["record_name_policy"] == "Strict Hostname Checking"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref)
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "sharedrecordgroup/ZG5z:my-group",
                "name": "my-group",
                "record_name_policy": "Strict Hostname Checking",
                "use_record_name_policy": True,
                "comment": "shared group",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecordgroup/ZG5z:my-group"
        g = await c.dns.sharedrecordgroup.get(ref)
        assert g.name == "my-group"
        assert g.record_name_policy == "Strict Hostname Checking"
        assert g.comment == "shared group"


# ---------------------------------------------------------------------------
# 3. find_one
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecordgroup/ZG5z:my-group",
                        "name": "my-group",
                        "record_name_policy": "Strict Hostname Checking",
                        "use_record_name_policy": True,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.sharedrecordgroup.find_one(name="my-group")
        assert g is not None
        assert g.name == "my-group"


# ---------------------------------------------------------------------------
# 4. create
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecordgroup/NEW:my-group",
                "name": "my-group",
                "record_name_policy": "Allow Underscore",
                "use_record_name_policy": False,
                "comment": "new group",
            }
        )

    async with _client(handler) as c:
        g = await c.dns.sharedrecordgroup.create(
            {
                "name": "my-group",
                "record_name_policy": "Allow Underscore",
                "comment": "new group",
            }
        )
        assert g.name == "my-group"
        assert g.record_name_policy == "Allow Underscore"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"my-group"' in body
        assert '"record_name_policy":"Allow Underscore"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 5. update_strips_readonly
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecordgroup/ZG5z:my-group",
                "name": "my-group",
                "record_name_policy": "Strict Hostname Checking",
                "use_record_name_policy": True,
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecordgroup/ZG5z:my-group"
        g = Sharedrecordgroup(
            name="my-group",
            record_name_policy="Strict Hostname Checking",
            use_record_name_policy=True,
            comment="updated",
            uuid="abc-123",  # RO
        )
        await c.dns.sharedrecordgroup.update(ref, g)
        body = captured[0].content.decode()

        assert '"uuid"' not in body, "uuid is readonly - must be stripped"
        assert '"name":"my-group"' in body
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 6. delete
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("sharedrecordgroup/ZG5z:my-group")

    async with _client(handler) as c:
        result = await c.dns.sharedrecordgroup.delete("sharedrecordgroup/ZG5z:my-group")
        assert result == "sharedrecordgroup/ZG5z:my-group"


# ---------------------------------------------------------------------------
# 7. extattrs round-trip
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_extattrs_round_trip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "sharedrecordgroup/ZG5z:my-group",
                        "name": "my-group",
                        "record_name_policy": "Strict Hostname Checking",
                        "use_record_name_policy": True,
                        "comment": "",
                        "extattrs": {"Team": {"value": "netops"}},
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        groups = await c.dns.sharedrecordgroup.list().all()
        g = groups[0]
        assert g.extattrs is not None
        assert g.extattrs["Team"].value == "netops"


# ---------------------------------------------------------------------------
# 8. set_extattrs helper
# ---------------------------------------------------------------------------


async def test_sharedrecordgroup_set_extattrs() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "sharedrecordgroup/ZG5z:my-group",
                "name": "my-group",
                "record_name_policy": "Strict Hostname Checking",
                "use_record_name_policy": True,
                "extattrs": {"Team": {"value": "netops"}},
            }
        )

    async with _client(handler) as c:
        ref = "sharedrecordgroup/ZG5z:my-group"
        await c.dns.sharedrecordgroup.set_extattrs(ref, Team="netops")

        req = captured[0]
        assert req.method == "PUT"
        body_data = json.loads(req.content.decode())
        assert body_data["extattrs"]["Team"]["value"] == "netops"
