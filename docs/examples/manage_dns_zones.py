# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS authoritative DNS zones (zone_auth).

List, create, update, delete authoritative zones, copy records between zones,
and lock/unlock zones for editing via the ibx-nios-sdk WAPI client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # List all authoritative zones
    python manage_dns_zones.py list

    # List zones filtered by FQDN substring and view
    python manage_dns_zones.py list --fqdn-like example --view default

    # Get a specific zone by ref
    python manage_dns_zones.py get zone_auth/ZG5z...

    # Create an authoritative zone
    python manage_dns_zones.py create --fqdn example.com --view default

    # Update a zone comment
    python manage_dns_zones.py update zone_auth/ZG5z... --comment "Updated"

    # Delete a zone
    python manage_dns_zones.py delete zone_auth/ZG5z...

    # Copy records from source zone into target zone
    python manage_dns_zones.py copy-records zone_auth/ZG5z... source.example.com

    # Lock a zone for editing
    python manage_dns_zones.py lock-unlock zone_auth/ZG5z... --lock
"""

import asyncio
import json

import click

from ibx_nios_sdk import NiosClient


def _dump_json(items):
    """Emit a JSON array of pydantic models (or dicts) to stdout."""
    payload = []
    for item in items:
        if hasattr(item, "model_dump"):
            payload.append(item.model_dump(mode="json", exclude_none=True, by_alias=True))
        else:
            payload.append(item)
    click.echo(json.dumps(payload, indent=2, default=str))


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
    """Manage NIOS authoritative DNS zones."""


@cli.command("list")
@_shared_options
@click.option("--fqdn-like", default=None, help="Substring filter on zone FQDN.")
@click.option("--view", default=None, help="Filter by DNS view name.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_cmd(grid_url, username, password, wapi_ver, verify, fqdn_like, view, json_output):
    """List authoritative zones."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if fqdn_like:
                filters["fqdn__like"] = fqdn_like
            if view:
                filters["view"] = view
            if json_output:
                rows = [z async for z in client.dns.zone_auth.list(**filters)]
                _dump_json(rows)
                return
            count = 0
            click.echo(f"{'FQDN':<45} {'View':<15} {'Format':<8} {'Disabled':<8} {'Comment'}")
            click.echo("-" * 100)
            async for z in client.dns.zone_auth.list(**filters):
                click.echo(
                    f"{(z.fqdn or '')[:44]:<45} "
                    f"{(z.view or 'default'):<15} "
                    f"{(z.zone_format or ''):<8} "
                    f"{str(z.disable or False):<8} "
                    f"{z.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("get")
@_shared_options
@click.argument("ref")
def get_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Get a single authoritative zone by reference.

    \b
    REF - WAPI object reference (e.g. zone_auth/ZG5z...:example.com/default)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            z = await client.dns.zone_auth.get(ref)
            click.echo(f"  ref:         {z.ref}")
            click.echo(f"  fqdn:        {z.fqdn}")
            click.echo(f"  view:        {z.view or 'default'}")
            click.echo(f"  zone_format: {z.zone_format}")
            click.echo(f"  disable:     {z.disable}")
            click.echo(f"  comment:     {z.comment or ''}")

    asyncio.run(run())


@cli.command("create")
@_shared_options
@click.option("--fqdn", required=True, help="Fully-qualified domain name for the zone.")
@click.option("--view", default=None, help="DNS view name (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
@click.option(
    "--zone-format",
    default="FORWARD",
    type=click.Choice(["FORWARD", "IPV4", "IPV6"]),
    show_default=True,
    help="Zone format.",
)
def create_cmd(grid_url, username, password, wapi_ver, verify, fqdn, view, comment, zone_format):
    """Create a new authoritative zone."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"fqdn": fqdn, "zone_format": zone_format}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            z = await client.dns.zone_auth.create(payload)
            click.echo(f"Created zone: {z.fqdn}")
            click.echo(f"  ref:  {z.ref}")
            click.echo(f"  view: {z.view or 'default'}")

    asyncio.run(run())


@cli.command("update")
@_shared_options
@click.argument("ref")
@click.option("--comment", default=None, help="New comment value.")
@click.option("--disable/--enable", default=None, help="Disable or enable the zone.")
def update_cmd(grid_url, username, password, wapi_ver, verify, ref, comment, disable):
    """Update an authoritative zone.

    \b
    REF - WAPI object reference for the zone to update
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            updates = {}
            if comment is not None:
                updates["comment"] = comment
            if disable is not None:
                updates["disable"] = disable
            if not updates:
                raise click.ClickException(
                    "Provide at least one field to update (--comment, --disable/--enable)."
                )
            z = await client.dns.zone_auth.update(ref, updates)
            click.echo(f"Updated zone: {z.fqdn}")
            click.echo(f"  ref:     {z.ref}")
            click.echo(f"  comment: {z.comment or ''}")
            click.echo(f"  disable: {z.disable}")

    asyncio.run(run())


@cli.command("delete")
@_shared_options
@click.argument("ref")
def delete_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an authoritative zone.

    \b
    REF - WAPI object reference for the zone to delete
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dns.zone_auth.delete(ref)
            click.echo(f"Deleted zone: {ref}")

    asyncio.run(run())


@cli.command("copy-records")
@_shared_options
@click.argument("ref")
@click.argument("source_zone")
@click.option("--view", default=None, help="DNS view scoping the source zone lookup.")
@click.option(
    "--copy-all-records/--no-copy-all-records",
    default=None,
    help="Copy all record types (default: WAPI selective copy).",
)
def copy_records_cmd(
    grid_url, username, password, wapi_ver, verify, ref, source_zone, view, copy_all_records
):
    """Copy DNS records from SOURCE_ZONE into the target zone REF.

    \b
    REF         - WAPI ref of the target zone_auth to copy records *into*
    SOURCE_ZONE - FQDN of the zone to copy records *from*
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            kwargs = {}
            if view is not None:
                kwargs["view"] = view
            if copy_all_records is not None:
                kwargs["copy_all_records"] = copy_all_records
            result = await client.dns.zone_auth.copy_zone_records(
                ref, source_zone=source_zone, **kwargs
            )
            click.echo(f"Copied records from '{source_zone}' into {ref}")
            if result:
                click.echo(f"  Result: {result}")

    asyncio.run(run())


@cli.command("lock-unlock")
@_shared_options
@click.argument("ref")
@click.option(
    "--lock/--unlock", required=True, help="Lock (--lock) or unlock (--unlock) the zone."
)
def lock_unlock_cmd(grid_url, username, password, wapi_ver, verify, ref, lock):
    """Lock or unlock a zone for editing.

    \b
    REF - WAPI object reference for the zone
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            result = await client.dns.zone_auth.lock_unlock_zone(ref, lock=lock)
            action = "Locked" if lock else "Unlocked"
            click.echo(f"{action} zone: {ref}")
            if result:
                click.echo(f"  Result: {result}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
