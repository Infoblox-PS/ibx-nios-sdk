# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Response Policy Zones (RPZ) and RPZ records.

Create and manage RPZ zones (zone_rp) and the full range of RPZ record types -
A substitution, CNAME block/redirect, and IP-address-based policy records.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables:
    NIOS_GRID_URL      - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME      - Admin username
    NIOS_PASSWORD      - Admin password
    NIOS_WAPI_VERSION  - Optional; default 2.14

Examples:
    # List all RPZ zones
    python manage_rpz.py list-zones

    # Create an RPZ zone
    python manage_rpz.py create-zone --fqdn malware.rpz.example.com --view default

    # Delete an RPZ zone by ref
    python manage_rpz.py delete-zone zone_rp/ZG5z...:malware.rpz.example.com/default

    # List RPZ A records in a zone
    python manage_rpz.py list-a-records --zone malware.rpz.example.com

    # Create an RPZ A record (substitute IP)
    python manage_rpz.py create-a-record --zone malware.rpz.example.com --name bad.example.com --ipv4addr 10.0.0.1

    # Block a name by CNAME to walled garden (empty canonical = NXDOMAIN)
    python manage_rpz.py create-cname-block --zone malware.rpz.example.com --name phish.example.com

    # Block an entire IP range via IP-address trigger
    python manage_rpz.py create-ip-block --zone malware.rpz.example.com --ipv4-network 192.0.2.0/24

    # Delete an RPZ record by ref
    python manage_rpz.py delete-record record:rpz:a/ZG5z...
"""

import asyncio

import click

from ibx_nios_sdk import NiosClient


def _connect(grid_url, username, password, wapi_ver, verify):
    return NiosClient(
        grid_url=grid_url,
        username=username,
        password=password,
        wapi_version=wapi_ver,
        verify=verify,
    )


def _shared_options(f):
    """Decorator that adds common connection options to a subcommand."""
    f = click.option(
        "--grid-url",
        envvar="NIOS_GRID_URL",
        required=True,
        help="Grid Manager URL (e.g. https://gm.example.com). Falls back to NIOS_GRID_URL.",
    )(f)
    f = click.option(
        "--username",
        envvar="NIOS_USERNAME",
        required=True,
        help="NIOS admin username. Falls back to NIOS_USERNAME.",
    )(f)
    f = click.option(
        "--password",
        envvar="NIOS_PASSWORD",
        required=True,
        hide_input=True,
        help="NIOS admin password. Falls back to NIOS_PASSWORD.",
    )(f)
    f = click.option(
        "--wapi-ver",
        envvar="NIOS_WAPI_VERSION",
        default="2.14",
        show_default=True,
        help="NIOS WAPI version (default 2.14). Falls back to NIOS_WAPI_VERSION.",
    )(f)
    f = click.option(
        "--verify/--no-verify",
        default=True,
        show_default=True,
        help="Verify TLS certificates. Use --no-verify for lab grids with self-signed certs.",
    )(f)
    return f


@click.group()
def cli():
    """Manage NIOS Response Policy Zones and RPZ records."""


@cli.command("list-zones")
@_shared_options
@click.option("--view", default=None, help="Filter by DNS view name.")
def list_zones(grid_url, username, password, wapi_ver, verify, view):
    """List RPZ zones with FQDN, view, type, and policy."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if view:
                filters["view"] = view
            count = 0
            click.echo(f"{'FQDN':<40} {'View':<12} {'RPZ Type':<18} {'Policy':<18} {'Disabled'}")
            click.echo("-" * 100)
            async for z in client.dns.zone_rp.list(**filters):
                click.echo(
                    f"{(z.fqdn or ''):<40} "
                    f"{(z.view or 'default'):<12} "
                    f"{(z.rpz_type or ''):<18} "
                    f"{(z.rpz_policy or ''):<18} "
                    f"{str(z.disable or False)}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-zone")
@_shared_options
@click.option("--fqdn", required=True, help="Fully-qualified domain name for the RPZ zone.")
@click.option("--view", default="default", show_default=True, help="DNS view name.")
@click.option(
    "--rpz-type",
    default="LOCAL",
    show_default=True,
    type=click.Choice(["LOCAL", "FEED", "ANALYTICS"]),
    help="RPZ zone type.",
)
@click.option("--substitute-name", default=None, help="Substitute name for GIVEN_IP policy.")
@click.option("--comment", default=None, help="Optional comment.")
def create_zone(
    grid_url, username, password, wapi_ver, verify, fqdn, view, rpz_type, substitute_name, comment
):
    """Create an RPZ zone."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload: dict = {"fqdn": fqdn, "view": view, "rpz_type": rpz_type}
            if substitute_name:
                payload["substitute_name"] = substitute_name
            if comment:
                payload["comment"] = comment
            z = await client.dns.zone_rp.create(payload)
            click.echo(f"Created RPZ zone: {z.fqdn}")
            click.echo(f"  ref:  {z.ref}")
            click.echo(f"  view: {z.view or 'default'}")

    asyncio.run(run())


@cli.command("delete-zone")
@_shared_options
@click.argument("ref")
def delete_zone(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an RPZ zone by WAPI reference.

    \b
    REF - WAPI object reference (e.g. zone_rp/ZG5z...:malware.rpz/default)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dns.zone_rp.delete(ref)
            click.echo(f"Deleted RPZ zone: {ref}")

    asyncio.run(run())


@cli.command("list-a-records")
@_shared_options
@click.option("--zone", required=True, help="RPZ zone FQDN to filter records by.")
def list_a_records(grid_url, username, password, wapi_ver, verify, zone):
    """List RPZ A records (name-to-IP substitutions) in a zone."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<45} {'IPv4 Addr':<18} {'Comment'}")
            click.echo("-" * 80)
            async for r in client.rpz.record_rpz_a.list(zone=zone):
                click.echo(f"{(r.name or ''):<45} {(r.ipv4addr or ''):<18} {r.comment or ''}")
                count += 1
            if count == 0:
                click.echo(f"No RPZ A records found in zone '{zone}'.")
            else:
                click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-a-record")
@_shared_options
@click.option("--zone", required=True, help="RPZ zone FQDN.")
@click.option("--name", required=True, help="Trigger name (relative to the RPZ zone).")
@click.option("--ipv4addr", required=True, help="Substitute IPv4 address.")
@click.option("--comment", default=None, help="Optional comment.")
def create_a_record(grid_url, username, password, wapi_ver, verify, zone, name, ipv4addr, comment):
    """Create an RPZ A record - substitute a matching name with an IP address."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload: dict = {"name": name, "rp_zone": zone, "ipv4addr": ipv4addr}
            if comment:
                payload["comment"] = comment
            r = await client.rpz.record_rpz_a.create(payload)
            click.echo(f"Created RPZ A record: {r.name} -> {r.ipv4addr}")
            click.echo(f"  ref:  {r.ref}")

    asyncio.run(run())


@cli.command("create-cname-block")
@_shared_options
@click.option("--zone", required=True, help="RPZ zone FQDN.")
@click.option("--name", required=True, help="Trigger name (relative to the RPZ zone).")
@click.option(
    "--canonical",
    default="",
    show_default=True,
    help="Canonical name. Empty string causes NXDOMAIN (block). Use '.' for NODATA.",
)
@click.option("--comment", default=None, help="Optional comment.")
def create_cname_block(
    grid_url, username, password, wapi_ver, verify, zone, name, canonical, comment
):
    """Create an RPZ CNAME record to block or redirect a name.

    An empty --canonical (the default) causes the zone to return NXDOMAIN for
    matching queries. Pass --canonical '.' for a NODATA (passthru) response.
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload: dict = {"name": name, "zone": zone, "canonical": canonical}
            if comment:
                payload["comment"] = comment
            r = await client.rpz.record_rpz_cname.create(payload)
            target = canonical if canonical else "(NXDOMAIN block)"
            click.echo(f"Created RPZ CNAME record: {r.name} -> {target}")
            click.echo(f"  ref:  {r.ref}")

    asyncio.run(run())


@cli.command("create-ip-block")
@_shared_options
@click.option("--zone", required=True, help="RPZ zone FQDN.")
@click.option(
    "--ipv4-network",
    required=True,
    metavar="CIDR",
    help="IPv4 network in CIDR notation (e.g. 192.0.2.0/24).",
)
@click.option("--comment", default=None, help="Optional comment.")
def create_ip_block(grid_url, username, password, wapi_ver, verify, zone, ipv4_network, comment):
    """Create an RPZ CNAME IP-address record to block responses to an IP range.

    Uses the record:rpz:cname:ipaddress object type which triggers on IP addresses
    in DNS responses, blocking entire subnets.
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # WAPI encodes the network in the name field as CIDR-encoded RPZ name
            payload: dict = {
                "name": ipv4_network,
                "zone": zone,
                "canonical": "",  # empty = NXDOMAIN
            }
            if comment:
                payload["comment"] = comment
            r = await client.rpz.record_rpz_cname_ipaddress.create(payload)
            click.echo(f"Created RPZ IP-block record for {ipv4_network} in zone '{zone}'")
            click.echo(f"  ref:  {r.ref}")

    asyncio.run(run())


@cli.command("delete-record")
@_shared_options
@click.argument("ref")
def delete_record(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an RPZ record by WAPI reference (auto-detects type from ref prefix).

    \b
    REF - WAPI object reference (e.g. record:rpz:a/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # Route to the correct resource based on the ref prefix
            ref_lower = ref.lower()
            if ref_lower.startswith("record:rpz:a:ipaddress/"):
                await client.rpz.record_rpz_a_ipaddress.delete(ref)
            elif ref_lower.startswith("record:rpz:a/"):
                await client.rpz.record_rpz_a.delete(ref)
            elif ref_lower.startswith("record:rpz:cname:ipaddress/"):
                await client.rpz.record_rpz_cname_ipaddress.delete(ref)
            elif ref_lower.startswith("record:rpz:cname/"):
                await client.rpz.record_rpz_cname.delete(ref)
            elif ref_lower.startswith("record:rpz:aaaa:ipaddress/"):
                await client.rpz.record_rpz_aaaa_ipaddress.delete(ref)
            elif ref_lower.startswith("record:rpz:aaaa/"):
                await client.rpz.record_rpz_aaaa.delete(ref)
            elif ref_lower.startswith("record:rpz:txt/"):
                await client.rpz.record_rpz_txt.delete(ref)
            elif ref_lower.startswith("record:rpz:mx/"):
                await client.rpz.record_rpz_mx.delete(ref)
            elif ref_lower.startswith("record:rpz:ptr/"):
                await client.rpz.record_rpz_ptr.delete(ref)
            elif ref_lower.startswith("record:rpz:srv/"):
                await client.rpz.record_rpz_srv.delete(ref)
            else:
                raise click.ClickException(
                    f"Unrecognised RPZ record ref prefix: {ref!r}\n"
                    "Supported: record:rpz:a, record:rpz:a:ipaddress, record:rpz:cname, "
                    "record:rpz:cname:ipaddress, record:rpz:aaaa, record:rpz:aaaa:ipaddress, "
                    "record:rpz:txt, record:rpz:mx, record:rpz:ptr, record:rpz:srv"
                )
            click.echo(f"Deleted RPZ record: {ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
