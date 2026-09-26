# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS DTC (Dynamic Traffic Control) servers.

Full CRUD lifecycle for DTC server objects. Servers represent the physical
or virtual endpoints that DTC balances traffic across.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as defaults):
    NIOS_GRID_URL      - Grid URL, e.g. https://192.168.1.2
    NIOS_USERNAME      - WAPI username
    NIOS_PASSWORD      - WAPI password
    NIOS_WAPI_VERSION  - WAPI version (default: 2.14)

Example usage:

    # List all servers
    python manage_dtc_servers.py list

    # Create a server with an IP address
    python manage_dtc_servers.py create --name app-east --host 10.0.0.1

    # Get a server by its WAPI ref
    python manage_dtc_servers.py get dtc:server/ZG5z...:app-east

    # Update a server's comment
    python manage_dtc_servers.py update dtc:server/ZG5z...:app-east --comment "East coast"

    # Delete a server (prompts for confirmation)
    python manage_dtc_servers.py delete dtc:server/ZG5z...:app-east
"""

from __future__ import annotations

import asyncio

import click

from ibx_nios_sdk import NiosClient

# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def _connect(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> NiosClient:
    """Construct a NiosClient from the shared connection options."""
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@click.group()
def cli() -> None:
    """Manage NIOS DTC server objects (dtc:server).

    Servers are the individual endpoints that DTC routes traffic to. They are
    referenced by pools via the ``servers`` list, which specifies each server
    and its associated load-balancing ratio.
    """


@cli.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Filter servers whose name contains this string.")
def cmd_list(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name_like: str | None,
) -> None:
    """List DTC servers, optionally filtered by name substring."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like

            servers = await client.dtc.server.list(**filters).all()

            if not servers:
                click.echo("No DTC servers found.")
                return

            click.echo(f"{'Name':<25} {'Host':<20} {'Disabled':<10} {'Comment'}")
            click.echo("-" * 80)
            for s in servers:
                click.echo(
                    f"{s.name or '':<25} "
                    f"{s.host or '':<20} "
                    f"{str(s.disable or False):<10} "
                    f"{s.comment or ''}"
                )
            click.echo(f"\nTotal: {len(servers)} server(s)")

    asyncio.run(run())


@cli.command("get")
@_shared_options
@click.argument("ref")
def cmd_get(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
) -> None:
    """Get full details of a DTC server by its WAPI reference (REF).

    REF is the WAPI object reference, e.g. dtc:server/ZG5z...:app-east
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            server = await client.dtc.server.get(
                ref,
                return_fields_plus=["host", "disable", "monitors", "health"],
            )
            click.echo(f"  ref:      {server.ref}")
            click.echo(f"  name:     {server.name}")
            click.echo(f"  host:     {server.host}")
            click.echo(f"  disable:  {server.disable}")
            click.echo(f"  comment:  {server.comment}")
            if server.monitors:
                click.echo(f"  monitors: {server.monitors}")
            if server.health:
                click.echo(f"  health:   {server.health}")

    asyncio.run(run())


@cli.command("create")
@_shared_options
@click.option("--name", required=True, help="Display name for the DTC server.")
@click.option(
    "--host",
    required=True,
    help="IP address or FQDN of the server endpoint.",
)
@click.option("--comment", default=None, help="Optional comment (max 256 chars).")
@click.option(
    "--disable/--enable",
    default=False,
    show_default=True,
    help="Create the server in disabled state.",
)
def cmd_create(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    host: str,
    comment: str | None,
    disable: bool,
) -> None:
    """Create a new DTC server object."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {"name": name, "host": host}
            if comment:
                body["comment"] = comment
            if disable:
                body["disable"] = True

            server = await client.dtc.server.create(body, return_fields_plus=["host", "disable"])
            click.secho("  [OK] DTC server created", fg="green")
            click.echo(f"  ref:     {server.ref}")
            click.echo(f"  name:    {server.name}")
            click.echo(f"  host:    {server.host}")
            click.echo(f"  disable: {server.disable}")

    asyncio.run(run())


@cli.command("update")
@_shared_options
@click.argument("ref")
@click.option("--name", default=None, help="New display name.")
@click.option("--host", default=None, help="New host IP address or FQDN.")
@click.option("--comment", default=None, help="New comment.")
@click.option(
    "--disable/--enable",
    default=None,
    help="Disable or re-enable the server.",
)
def cmd_update(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
    name: str | None,
    host: str | None,
    comment: str | None,
    disable: bool | None,
) -> None:
    """Update fields on an existing DTC server (REF).

    REF is the WAPI object reference, e.g. dtc:server/ZG5z...:app-east.
    Only the options you provide are changed.
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {}
            if name is not None:
                body["name"] = name
            if host is not None:
                body["host"] = host
            if comment is not None:
                body["comment"] = comment
            if disable is not None:
                body["disable"] = disable

            if not body:
                raise click.UsageError(
                    "Provide at least one of --name, --host, --comment, --disable/--enable"
                )

            server = await client.dtc.server.update(
                ref, body, return_fields_plus=["host", "disable"]
            )
            click.secho("  [OK] DTC server updated", fg="green")
            click.echo(f"  ref:     {server.ref}")
            click.echo(f"  name:    {server.name}")
            click.echo(f"  host:    {server.host}")
            click.echo(f"  disable: {server.disable}")

    asyncio.run(run())


@cli.command("delete")
@_shared_options
@click.argument("ref")
def cmd_delete(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
) -> None:
    """Delete a DTC server by WAPI reference (REF).

    REF is the WAPI object reference, e.g. dtc:server/ZG5z...:app-east.
    You will be prompted to confirm before deletion.
    """

    async def run() -> None:
        click.confirm(f"Delete DTC server '{ref}'?", abort=True)
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            deleted = await client.dtc.server.delete(ref)
            click.secho(f"  [OK] Deleted: {deleted}", fg="green")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
