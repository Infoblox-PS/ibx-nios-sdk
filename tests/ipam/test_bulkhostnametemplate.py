# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""BulkhostnametemplateResource - CRUD, find_one, list, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.bulkhostnametemplate import Bulkhostnametemplate
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns bulkhostnametemplate objects
# ---------------------------------------------------------------------------


async def test_bulkhostnametemplate_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "bulkhostnametemplate/ZG5z:default",
                        "template_name": "default",
                        "template_format": "{n}",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        templates = await c.ipam.bulkhostnametemplate.list().all()
        assert len(templates) == 1
        t = templates[0]
        assert t.template_name == "default"
        assert t.template_format == "{n}"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "template_name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(template_name="default") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_bulkhostnametemplate_list_by_name() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "bulkhostnametemplate/ZG5z:default",
                        "template_name": "default",
                        "template_format": "{n}",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        templates = await c.ipam.bulkhostnametemplate.list(template_name="default").all()
        assert len(templates) == 1
        params = captured[0].url.params
        assert params.get("template_name") == "default"


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_bulkhostnametemplate_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "bulkhostnametemplate/ZG5z:default",
                "template_name": "default",
                "template_format": "{n}",
            }
        )

    async with _client(handler) as c:
        ref = "bulkhostnametemplate/ZG5z:default"
        t = await c.ipam.bulkhostnametemplate.get(ref)
        assert t.template_name == "default"
        assert t.template_format == "{n}"


# ---------------------------------------------------------------------------
# 4. find_one(template_name="default") - returns first match
# ---------------------------------------------------------------------------


async def test_bulkhostnametemplate_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "bulkhostnametemplate/ZG5z:default",
                        "template_name": "default",
                        "template_format": "{n}",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        t = await c.ipam.bulkhostnametemplate.find_one(template_name="default")
        assert t is not None
        assert t.template_name == "default"


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_bulkhostnametemplate_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "bulkhostnametemplate/ZG5z:custom",
                "template_name": "custom",
                "template_format": "host-{n}",
            }
        )

    async with _client(handler) as c:
        t = await c.ipam.bulkhostnametemplate.create(
            {"template_name": "custom", "template_format": "host-{n}"}
        )
        assert t.template_name == "custom"

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"template_name":"custom"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update strips readonly fields (is_grid_default, pre_defined, uuid)
# ---------------------------------------------------------------------------


async def test_bulkhostnametemplate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "bulkhostnametemplate/ZG5z:custom",
                "template_name": "custom",
                "template_format": "host-{n}",
            }
        )

    async with _client(handler) as c:
        ref = "bulkhostnametemplate/ZG5z:custom"
        tmpl = Bulkhostnametemplate(
            template_name="custom",
            template_format="host-{n}",
            is_grid_default=True,  # RO
            pre_defined=False,  # RO
            uuid="some-uuid",  # RO
        )
        await c.ipam.bulkhostnametemplate.update(ref, tmpl)
        body = json.loads(captured[0].content.decode())

        assert "is_grid_default" not in body, "is_grid_default is readonly - must be stripped"
        assert "pre_defined" not in body, "pre_defined is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("template_name") == "custom"
