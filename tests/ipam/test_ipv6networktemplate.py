# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networktemplateResource - CRUD, find_one, list, extattrs, readonly-strip."""

from __future__ import annotations

import json
from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.ipam.models.ipv6networktemplate import Ipv6networktemplate
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list() - returns ipv6networktemplate objects
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_list() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6networktemplate/ZG5z:default_ipv6_template",
                        "name": "default_ipv6_template",
                        "cidr": 64,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        templates = await c.ipam.ipv6networktemplate.list().all()
        assert len(templates) == 1
        t = templates[0]
        assert t.name == "default_ipv6_template"
        assert t.cidr == 64

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. list(name__like="corp") - filter applied correctly
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_list_name_like() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6networktemplate/ZG5z:corp_ipv6_template",
                        "name": "corp_ipv6_template",
                        "cidr": 64,
                        "comment": "Corporate IPv6",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        templates = await c.ipam.ipv6networktemplate.list(name__like="corp").all()
        assert len(templates) == 1
        assert templates[0].name == "corp_ipv6_template"

        params = captured[0].url.params
        assert any("corp" in v for v in params.values())


# ---------------------------------------------------------------------------
# 3. get(ref) - parses fields correctly
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "ipv6networktemplate/ZG5z:prod_ipv6_template",
                "name": "prod_ipv6_template",
                "cidr": 48,
                "comment": "Production IPv6 template",
            }
        )

    async with _client(handler) as c:
        ref = "ipv6networktemplate/ZG5z:prod_ipv6_template"
        t = await c.ipam.ipv6networktemplate.get(ref)
        assert t.name == "prod_ipv6_template"
        assert t.cidr == 48
        assert t.comment == "Production IPv6 template"


# ---------------------------------------------------------------------------
# 4. find_one(name="prod_ipv6_template") - returns first match
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "ipv6networktemplate/ZG5z:prod_ipv6_template",
                        "name": "prod_ipv6_template",
                        "cidr": 48,
                        "comment": "",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        t = await c.ipam.ipv6networktemplate.find_one(name="prod_ipv6_template")
        assert t is not None
        assert t.name == "prod_ipv6_template"
        assert t.cidr == 48


# ---------------------------------------------------------------------------
# 5. create - POST body correct
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6networktemplate/ZG5z:new_ipv6_template",
                "name": "new_ipv6_template",
                "cidr": 64,
                "comment": "New IPv6 template",
            }
        )

    async with _client(handler) as c:
        t = await c.ipam.ipv6networktemplate.create(
            {"name": "new_ipv6_template", "cidr": 64, "comment": "New IPv6 template"}
        )
        assert t.name == "new_ipv6_template"
        assert t.cidr == 64

        req = captured[0]
        assert req.method == "POST"
        body = req.content.decode()
        assert '"name":"new_ipv6_template"' in body
        assert req.url.params.get("_return_as_object") == "1"


# ---------------------------------------------------------------------------
# 6. update(ref, {...}) - PUT to /{ref}
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6networktemplate/ZG5z:prod_ipv6_template",
                "name": "prod_ipv6_template",
                "cidr": 48,
                "comment": "Updated comment",
            }
        )

    async with _client(handler) as c:
        ref = "ipv6networktemplate/ZG5z:prod_ipv6_template"
        t = await c.ipam.ipv6networktemplate.update(ref, {"comment": "Updated comment"})
        assert t.comment == "Updated comment"

        req = captured[0]
        assert req.method == "PUT"
        assert ref in req.url.path
        body = req.content.decode()
        assert '"comment":"Updated comment"' in body


# ---------------------------------------------------------------------------
# Extra: readonly-strip on update
# ---------------------------------------------------------------------------


async def test_ipv6networktemplate_update_strips_readonly() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "ipv6networktemplate/ZG5z:prod_ipv6_template",
                "name": "prod_ipv6_template",
                "cidr": 48,
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "ipv6networktemplate/ZG5z:prod_ipv6_template"
        tmpl = Ipv6networktemplate(
            name="prod_ipv6_template",
            comment="updated",
            rir="ARIN",  # RO
            uuid="some-uuid",  # RO
        )
        await c.ipam.ipv6networktemplate.update(ref, tmpl)
        body = json.loads(captured[0].content.decode())

        assert "rir" not in body, "rir is readonly - must be stripped"
        assert "uuid" not in body, "uuid is readonly - must be stripped"
        assert body.get("name") == "prod_ipv6_template"
        assert body.get("comment") == "updated"
