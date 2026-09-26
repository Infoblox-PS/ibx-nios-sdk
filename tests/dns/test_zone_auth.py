# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneAuthResource - CRUD, find_one, list, function calls, readonly-strip."""

from __future__ import annotations

from typing import Any

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.zone_auth import ZoneAuth
from tests.conftest import json_response


def _client(handler: Any) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


# ---------------------------------------------------------------------------
# 1. list(view="default") - filter param + parsed ZoneAuth instances
# ---------------------------------------------------------------------------


async def test_zone_auth_list_with_view_filter() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_auth/ZG5z:example.com/default",
                        "fqdn": "example.com",
                        "view": "default",
                        "zone_format": "FORWARD",
                        "comment": "",
                        "disable": False,
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        zones = await c.dns.zone_auth.list(view="default").all()
        assert len(zones) == 1
        z = zones[0]
        assert z.fqdn == "example.com"
        assert z.view == "default"

        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["view"] == "default"
        assert "fqdn" in params["_return_fields+"]


# ---------------------------------------------------------------------------
# 2. get(ref) - returns ZoneAuth with nested grid_primary list
# ---------------------------------------------------------------------------


async def test_zone_auth_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "_ref": "zone_auth/ZG5z:example.com/default",
                "fqdn": "example.com",
                "view": "default",
                "zone_format": "FORWARD",
                "comment": "main zone",
                "grid_primary": [
                    {
                        "name": "member1.infoblox.local",
                        "stealth": False,
                        "grid_replicate": True,
                        "lead": True,
                        "enable_preferred_primaries": False,
                    }
                ],
            }
        )

    async with _client(handler) as c:
        ref = "zone_auth/ZG5z:example.com/default"
        z = await c.dns.zone_auth.get(ref)
        assert z.fqdn == "example.com"
        assert z.view == "default"
        assert z.zone_format == "FORWARD"
        assert z.comment == "main zone"
        assert z.grid_primary is not None
        assert len(z.grid_primary) == 1
        assert z.grid_primary[0].name == "member1.infoblox.local"
        assert z.grid_primary[0].grid_replicate is True


# ---------------------------------------------------------------------------
# 3. find_one(fqdn="example.com")
# ---------------------------------------------------------------------------


async def test_zone_auth_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response(
            {
                "result": [
                    {
                        "_ref": "zone_auth/ZG5z:example.com/default",
                        "fqdn": "example.com",
                        "view": "default",
                    }
                ],
                "next_page_id": "",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_auth.find_one(fqdn="example.com")
        assert z is not None
        assert z.fqdn == "example.com"


# ---------------------------------------------------------------------------
# 4. create with nested grid_primary - verify POST body
# ---------------------------------------------------------------------------


async def test_zone_auth_create_with_grid_primary() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_auth/NEW:example.com/default",
                "fqdn": "example.com",
                "view": "default",
            }
        )

    async with _client(handler) as c:
        z = await c.dns.zone_auth.create(
            {
                "fqdn": "example.com",
                "view": "default",
                "grid_primary": [{"name": "member1"}],
            }
        )
        assert z.fqdn == "example.com"
        body = captured[0].content.decode()
        assert '"fqdn":"example.com"' in body
        assert '"view":"default"' in body
        assert '"grid_primary"' in body
        assert '"member1"' in body


# ---------------------------------------------------------------------------
# 5. update - verify PUT uses the ref in the path
# ---------------------------------------------------------------------------


async def test_zone_auth_update() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_auth/ZG5z:example.com/default",
                "fqdn": "example.com",
                "view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "zone_auth/ZG5z:example.com/default"
        z = await c.dns.zone_auth.update(ref, {"comment": "updated"})
        assert z.comment == "updated"
        # Verify PUT was sent to the correct ref path
        assert captured[0].method == "PUT"
        assert ref in captured[0].url.path


# ---------------------------------------------------------------------------
# 6. delete(ref) - returns the ref
# ---------------------------------------------------------------------------


async def test_zone_auth_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("zone_auth/ZG5z:example.com/default")

    async with _client(handler) as c:
        result = await c.dns.zone_auth.delete("zone_auth/ZG5z:example.com/default")
        assert result == "zone_auth/ZG5z:example.com/default"


# ---------------------------------------------------------------------------
# 7. call_function copyzonerecords - typed wrapper + raw call_function
# ---------------------------------------------------------------------------


async def test_zone_auth_copy_zone_records_function() -> None:
    """copy_zone_records posts to /{ref}?_function=copyzonerecords with correct body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"status": "ok"})

    async with _client(handler) as c:
        ref = "zone_auth/XYZ:example.com/default"
        result = await c.dns.zone_auth.copy_zone_records(
            ref,
            source_zone="template.example.com",
            view="default",
        )
        assert result == {"status": "ok"}

        req = captured[0]
        assert req.method == "POST"
        assert ref in req.url.path
        assert req.url.params["_function"] == "copyzonerecords"
        body = req.content.decode()
        assert '"zone":"template.example.com"' in body
        assert '"view":"default"' in body


# ---------------------------------------------------------------------------
# 8. Read-only fields are stripped from update body
# ---------------------------------------------------------------------------


async def test_zone_auth_update_strips_readonly() -> None:
    """Readonly fields (last_queried, dns_fqdn, locked_by, etc.) must not appear in PUT body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response(
            {
                "_ref": "zone_auth/ZG5z:example.com/default",
                "fqdn": "example.com",
                "view": "default",
                "comment": "updated",
            }
        )

    async with _client(handler) as c:
        ref = "zone_auth/ZG5z:example.com/default"
        # Construct a ZoneAuth with several readonly fields set
        z = ZoneAuth(
            fqdn="example.com",
            view="default",
            comment="updated",
            last_queried=1234567890,  # RO
            dns_fqdn="example.com.",  # RO
            locked_by="admin",  # RO
            is_dnssec_enabled=True,  # RO
            primary_type="GRID",  # RO
            network_view="default",  # RO
        )
        await c.dns.zone_auth.update(ref, z)
        body = captured[0].content.decode()

        # Readonly fields must not appear
        assert '"last_queried"' not in body, "last_queried is readonly - must be stripped"
        assert '"dns_fqdn"' not in body, "dns_fqdn is readonly - must be stripped"
        assert '"locked_by"' not in body, "locked_by is readonly - must be stripped"
        assert '"is_dnssec_enabled"' not in body, (
            "is_dnssec_enabled is readonly - must be stripped"
        )
        assert '"primary_type"' not in body, "primary_type is readonly - must be stripped"
        assert '"network_view"' not in body, "network_view is readonly - must be stripped"

        # Writable fields must be present
        assert '"comment":"updated"' in body


# ---------------------------------------------------------------------------
# 9. copy_zone_records with copy_all_records=True (line 40)
# ---------------------------------------------------------------------------


async def test_zone_auth_copy_zone_records_with_copy_all_records() -> None:
    """copy_zone_records with copy_all_records=True must include it in the POST body."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"status": "ok"})

    async with _client(handler) as c:
        ref = "zone_auth/XYZ:example.com/default"
        result = await c.dns.zone_auth.copy_zone_records(
            ref,
            source_zone="template.example.com",
            copy_all_records=True,
        )
        assert result == {"status": "ok"}

        body = captured[0].content.decode()
        assert '"copy_all_records":true' in body or '"copy_all_records": true' in body


# ---------------------------------------------------------------------------
# 10. lock_unlock_zone (line 50)
# ---------------------------------------------------------------------------


async def test_zone_auth_lock_unlock_zone() -> None:
    """lock_unlock_zone must POST to /{ref}?_function=lock_unlock_zone with operation."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"status": "locked"})

    async with _client(handler) as c:
        ref = "zone_auth/XYZ:example.com/default"
        result = await c.dns.zone_auth.lock_unlock_zone(ref, lock=True)
        assert result == {"status": "locked"}

        req = captured[0]
        assert req.method == "POST"
        assert ref in req.url.path
        assert req.url.params["_function"] == "lock_unlock_zone"
        body = req.content.decode()
        assert '"operation":"LOCK"' in body or '"operation": "LOCK"' in body


async def test_zone_auth_unlock_zone() -> None:
    """lock_unlock_zone with lock=False must send operation=UNLOCK."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("Authorization", "").startswith("Basic "):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"status": "unlocked"})

    async with _client(handler) as c:
        ref = "zone_auth/XYZ:example.com/default"
        result = await c.dns.zone_auth.lock_unlock_zone(ref, lock=False)
        assert result == {"status": "unlocked"}

        body = captured[0].content.decode()
        assert '"operation":"UNLOCK"' in body or '"operation": "UNLOCK"' in body
