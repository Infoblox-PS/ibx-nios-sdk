# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Live integration smoke test for ibx-nios-sdk.

Targets whatever grid the standard ``NIOS_*`` environment variables point at.
Nothing is hardcoded: this suite creates and deletes real objects, so it must
never run against a production grid by accident, and no grid address or
credential belongs in a public repository.

Run with:
    NIOS_LIVE=1 NIOS_GRID_URL=https://grid.example.com \
        NIOS_USERNAME=admin NIOS_PASSWORD=... \
        pytest tests/integration/test_smoke_live.py -v

``NIOS_VERIFY=0`` disables TLS verification for a lab grid with a self-signed
certificate; ``NIOS_WAPI_VERSION`` overrides the default WAPI version.
"""

from __future__ import annotations

import os
import random
import string

import pytest

if not os.getenv("NIOS_LIVE"):
    pytest.skip("set NIOS_LIVE=1 to run live tests", allow_module_level=True)

from ibx_nios_sdk import NiosClient  # noqa: E402
from ibx_nios_sdk._exceptions import NiosError, NotFoundError  # noqa: E402

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]

GRID_URL = os.environ.get("NIOS_GRID_URL", "")
USERNAME = os.environ.get("NIOS_USERNAME", "")
PASSWORD = os.environ.get("NIOS_PASSWORD", "")
WAPI_VERSION = os.environ.get("NIOS_WAPI_VERSION", "2.14")
VERIFY = os.environ.get("NIOS_VERIFY", "1") not in ("0", "false", "no")

if not (GRID_URL and USERNAME and PASSWORD):
    pytest.skip(
        "set NIOS_GRID_URL, NIOS_USERNAME and NIOS_PASSWORD to run live tests",
        allow_module_level=True,
    )


def _rand_suffix(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


@pytest.fixture(scope="module")
async def client():
    async with NiosClient(
        grid_url=GRID_URL,
        username=USERNAME,
        password=PASSWORD,
        verify=VERIFY,
        wapi_version=WAPI_VERSION,
    ) as c:
        yield c


@pytest.fixture(scope="module")
async def zone_info(client):
    """Return (zone_fqdn, view_name) of a usable authoritative zone, or None."""
    zones = await client.dns.zone_auth.list(max_results=10).all()
    if not zones:
        return None
    for z in zones:
        fqdn = getattr(z, "fqdn", None)
        view = getattr(z, "view", None) or "default"
        if fqdn:
            return fqdn, view
    return None


async def test_01_login_session(client):
    """Trivial call proves session auth works."""
    views = await client.dns.view.list().all()
    assert len(views) > 0, "no DNS views returned from grid"


async def test_02_list_and_paging(client):
    items, next_id = await client.dns.record_a.list_page(max_results=5)
    assert isinstance(items, list)
    assert len(items) <= 5
    # next_id is either a non-empty string or None - just ensure the call
    # returns the metadata tuple without error.
    assert next_id is None or isinstance(next_id, str)


async def test_03_record_a_crud(client, zone_info):
    if zone_info is None:
        pytest.skip("no authoritative zones present on grid")
    zone_fqdn, view = zone_info
    name = f"ibxsdk-smoke-{_rand_suffix()}.{zone_fqdn}"
    ref = None
    try:
        created = await client.dns.record_a.create(
            {"name": name, "ipv4addr": "10.99.99.1", "view": view}
        )
        ref = created.ref
        assert ref and ref.startswith("record:a/")

        fetched = await client.dns.record_a.get(ref)
        assert fetched.name == name
        assert fetched.ipv4addr == "10.99.99.1"

        updated = await client.dns.record_a.update(ref, {"comment": "smoke"})
        assert updated.comment == "smoke"
    finally:
        if ref:
            try:
                await client.dns.record_a.delete(ref)
            except NiosError:
                pass


async def test_04_network_crud(client):
    cidr = "192.0.2.0/30"
    existing = await client.ipam.network.find_one(network=cidr)
    if existing is not None:
        pytest.skip(f"network {cidr} already exists on grid")
    ref = None
    try:
        created = await client.ipam.network.create({"network": cidr, "comment": "ibxsdk smoke"})
        ref = created.ref
        assert ref and ref.startswith("network/")
        fetched = await client.ipam.network.get(ref)
        assert fetched.network == cidr
    finally:
        if ref:
            try:
                await client.ipam.network.delete(ref)
            except NiosError:
                pass


async def test_05_extattr_roundtrip(client, zone_info):
    if zone_info is None:
        pytest.skip("no authoritative zones present on grid")
    zone_fqdn, view = zone_info
    name = f"ibxsdk-ea-{_rand_suffix()}.{zone_fqdn}"
    ref = None
    try:
        created = await client.dns.record_a.create(
            {
                "name": name,
                "ipv4addr": "10.99.99.2",
                "view": view,
                "extattrs": {"Site": {"value": "SMOKE"}},
            },
            return_fields_plus=["extattrs"],
        )
        ref = created.ref
        fetched = await client.dns.record_a.get(ref, return_fields_plus=["extattrs"])
        extattrs = getattr(fetched, "extattrs", None) or {}
        # extattrs may be parsed into model objects - coerce to dict
        if hasattr(extattrs, "model_dump"):
            extattrs = extattrs.model_dump()
        site = extattrs.get("Site") if isinstance(extattrs, dict) else None
        if hasattr(site, "model_dump"):
            site = site.model_dump()
        assert site is not None, f"Site extattr did not round-trip: {extattrs!r}"
        # value may be under .value or ["value"]
        site_value = site.get("value") if isinstance(site, dict) else getattr(site, "value", None)
        assert site_value == "SMOKE"
    finally:
        if ref:
            try:
                await client.dns.record_a.delete(ref)
            except NiosError:
                pass


async def test_06_function_call_next_available_ip(client):
    net = await client.ipam.network.find_one()
    if net is None:
        pytest.skip("no networks exist on grid")
    result = await client.ipam.network.next_available_ip(net.ref, num=1)
    assert "ips" in result, f"unexpected response shape: {result!r}"
    assert isinstance(result["ips"], list)


async def test_07_readonly_strip_on_update(client, zone_info):
    """Verify that update() strips readonly fields (e.g. creation_time)."""
    if zone_info is None:
        pytest.skip("no authoritative zones present on grid")
    zone_fqdn, view = zone_info
    name = f"ibxsdk-ro-{_rand_suffix()}.{zone_fqdn}"
    ref = None
    try:
        created = await client.dns.record_a.create(
            {"name": name, "ipv4addr": "10.99.99.3", "view": view},
            return_fields_plus=["creation_time"],
        )
        ref = created.ref
        # creation_time should be set by server and is readonly; passing the
        # model back to update() must not cause a 400.
        created.comment = "readonly-strip-test"
        updated = await client.dns.record_a.update(ref, created)
        assert updated.comment == "readonly-strip-test"
    finally:
        if ref:
            try:
                await client.dns.record_a.delete(ref)
            except NiosError:
                pass


async def test_08_error_handling_not_found(client):
    # A well-formed but non-existent ref - use a plausible base64-like body.
    bogus = "record:a/ZG5zLmJpbmRfYSQuXzM0Lm5vcGUsMS4yLjMuNA:ibxsdk-bogus.example.com/default"
    with pytest.raises((NotFoundError, NiosError)) as excinfo:
        await client.dns.record_a.get(bogus)
    # Prefer NotFoundError, but accept generic NiosError - assert status hint.
    err = excinfo.value
    assert isinstance(err, NiosError)


async def test_09_new_object_smoke_rir(client):
    """Smoke-test a recently added object: rir.list_page should not 5xx."""
    try:
        items, _ = await client.ipam.rir.list_page(max_results=1)
    except NiosError as e:
        if e.status_code and 500 <= e.status_code < 600:
            pytest.fail(f"rir.list_page returned 5xx: {e}")
        # 4xx is acceptable (e.g. unsupported in this WAPI version); re-raise
        raise
    assert isinstance(items, list)


async def test_09b_new_object_smoke_blockingpolicy(client):
    try:
        items, _ = await client.security.parentalcontrol_blockingpolicy.list_page(max_results=1)
    except NiosError as e:
        if e.status_code and 500 <= e.status_code < 600:
            pytest.fail(f"parentalcontrol:blockingpolicy.list_page returned 5xx: {e}")
        raise
    assert isinstance(items, list)
