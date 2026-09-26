# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Grid configuration, extensible-attribute definitions, and services.

List and inspect the grid object, manage custom extensible-attribute definitions,
and trigger grid-wide service restarts via the ibx-nios-sdk WAPI client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables:
    NIOS_GRID_URL      - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME      - Admin username
    NIOS_PASSWORD      - Admin password
    NIOS_WAPI_VERSION  - Optional; default 2.14

Examples:
    # Show the single Grid object
    python manage_grid.py show-grid

    # List all extensible-attribute definitions
    python manage_grid.py list-ea-defs

    # Create a STRING extensible attribute
    python manage_grid.py create-ea-def Site --type STRING --comment "Datacenter site"

    # Create a LIST extensible attribute with allowed values
    python manage_grid.py create-ea-def Environment --type STRING --list-values prod staging dev

    # Delete an extensible-attribute definition by ref
    python manage_grid.py delete-ea-def extensibleattributedef/ZG5z...:Site

    # Restart DNS and DHCP services grid-wide
    python manage_grid.py restart-grid-services --services DNS DHCP
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
    """Manage NIOS Grid configuration and extensible-attribute definitions."""


@cli.command("show-grid")
@_shared_options
def show_grid(grid_url, username, password, wapi_ver, verify):
    """Show the single Grid object configuration."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            grids = await client.grid.grid.list().all()
            if not grids:
                raise click.ClickException("No grid object found.")
            g = grids[0]
            click.echo(f"  ref:     {g.ref}")
            click.echo(f"  name:    {g.name}")

    asyncio.run(run())


@cli.command("list-grids")
@_shared_options
def list_grids(grid_url, username, password, wapi_ver, verify):
    """List Grid objects (typically one per deployment)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<30} {'Ref'}")
            click.echo("-" * 60)
            async for g in client.grid.grid.list():
                click.echo(f"{(g.name or ''):<30} {g.ref or ''}")
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("list-ea-defs")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on attribute name.")
def list_ea_defs(grid_url, username, password, wapi_ver, verify, name_like):
    """List extensible-attribute definitions."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Name':<30} {'Type':<12} {'Flags':<8} {'Comment'}")
            click.echo("-" * 80)
            async for ea in client.grid.extensibleattributedef.list(**filters):
                click.echo(
                    f"{(ea.name or ''):<30} "
                    f"{(ea.type_ or ''):<12} "
                    f"{(ea.flags or ''):<8} "
                    f"{ea.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-ea-def")
@_shared_options
@click.argument("name")
@click.option(
    "--type",
    "ea_type",
    required=True,
    type=click.Choice(["STRING", "INTEGER", "EMAIL", "URL", "DATE", "ENUM"]),
    help="Extensible attribute type.",
)
@click.option("--comment", default=None, help="Optional comment.")
@click.option("--flags", default=None, help="Attribute flags (e.g. 'C' for cloud-safe).")
@click.option(
    "--list-values",
    multiple=True,
    metavar="VALUE",
    help="Allowed values for ENUM type (repeatable).",
)
def create_ea_def(
    grid_url, username, password, wapi_ver, verify, name, ea_type, comment, flags, list_values
):
    """Create a custom extensible-attribute definition.

    \b
    NAME - Name of the new extensible-attribute definition
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload: dict = {"name": name, "type": ea_type}
            if comment:
                payload["comment"] = comment
            if flags:
                payload["flags"] = flags
            if list_values:
                payload["list_values"] = [{"value": v} for v in list_values]
            ea = await client.grid.extensibleattributedef.create(payload)
            click.echo(f"Created extensible-attribute definition: {ea.name}")
            click.echo(f"  ref:  {ea.ref}")
            click.echo(f"  type: {ea.type_}")

    asyncio.run(run())


@cli.command("delete-ea-def")
@_shared_options
@click.argument("ref")
def delete_ea_def(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an extensible-attribute definition by WAPI reference.

    \b
    REF - WAPI object reference (e.g. extensibleattributedef/ZG5z...:Site)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.grid.extensibleattributedef.delete(ref)
            click.echo(f"Deleted extensible-attribute definition: {ref}")

    asyncio.run(run())


@cli.command("restart-grid-services")
@_shared_options
@click.option(
    "--services",
    multiple=True,
    metavar="SERVICE",
    help="Service names to restart (e.g. DNS DHCP). Omit for all services.",
)
@click.option(
    "--restart-option",
    default="RESTART_IF_NEEDED",
    show_default=True,
    type=click.Choice(["RESTART_IF_NEEDED", "FORCE_RESTART", "RELOAD_ALL", "RESTART_ALL"]),
    help="Restart trigger policy.",
)
@click.option(
    "--member-order",
    default="SIMULTANEOUSLY",
    show_default=True,
    type=click.Choice(["SIMULTANEOUSLY", "SEQUENTIALLY"]),
    help="Order in which members restart.",
)
def restart_grid_services(
    grid_url, username, password, wapi_ver, verify, services, restart_option, member_order
):
    """Restart services across all Grid members."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            grids = await client.grid.grid.list().all()
            if not grids:
                raise click.ClickException("No grid object found.")
            ref = grids[0].ref
            svc_list = list(services) if services else None
            result = await client.grid.grid.restart_services(
                ref,
                member_order=member_order,
                restart_option=restart_option,
                services=svc_list,
            )
            svc_label = ", ".join(services) if services else "ALL"
            click.echo(f"Restarted services [{svc_label}] on grid {ref}")
            if result:
                click.echo(f"  Result: {result}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
