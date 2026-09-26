# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Grid members - list, inspect, and restart services.

Query Grid member objects, retrieve per-member details, trigger per-member
service restarts, and view grid-wide restart status via the ibx-nios-sdk client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables:
    NIOS_GRID_URL      - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME      - Admin username
    NIOS_PASSWORD      - Admin password
    NIOS_WAPI_VERSION  - Optional; default 2.14

Examples:
    # List all Grid members
    python manage_members.py list

    # List members filtered by name substring
    python manage_members.py list --name-like gm1

    # List members of a specific platform type
    python manage_members.py list --platform VNIOS

    # Get full details for a specific member
    python manage_members.py get gm1.example.com

    # Restart DNS on a specific member
    python manage_members.py restart-services gm1.example.com --services DNS

    # View current restart status across the grid
    python manage_members.py list-restart-status
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
    """Manage NIOS Grid members."""


@cli.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on host_name.")
@click.option("--platform", default=None, help="Filter by platform type (e.g. VNIOS, PHYSICAL).")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_cmd(grid_url, username, password, wapi_ver, verify, name_like, platform, json_output):
    """List Grid members with hostname, platform, and service config."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["host_name__like"] = name_like
            if platform:
                filters["platform"] = platform
            if json_output:
                rows = [m async for m in client.grid.member.list(**filters)]
                _dump_json(rows)
                return
            count = 0
            click.echo(f"{'Hostname':<35} {'Platform':<12} {'Service Config':<18} {'Comment'}")
            click.echo("-" * 90)
            async for m in client.grid.member.list(**filters):
                click.echo(
                    f"{(m.host_name or ''):<35} "
                    f"{(m.platform or ''):<12} "
                    f"{(m.service_type_configuration or ''):<18} "
                    f"{m.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("get")
@_shared_options
@click.argument("name")
def get_cmd(grid_url, username, password, wapi_ver, verify, name):
    """Get full details for a Grid member by hostname.

    \b
    NAME - Hostname of the Grid member (e.g. gm1.example.com)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            member = await client.grid.member.find_one(host_name=name)
            if member is None:
                raise click.ClickException(f"No member found with host_name '{name}'.")
            click.echo(json.dumps(member.model_dump(exclude_none=True), indent=2, default=str))

    asyncio.run(run())


@cli.command("restart-services")
@_shared_options
@click.argument("member_name")
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
def restart_services(
    grid_url, username, password, wapi_ver, verify, member_name, services, restart_option
):
    """Restart services on a specific Grid member.

    \b
    MEMBER_NAME - Hostname of the Grid member (e.g. gm1.example.com)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            member = await client.grid.member.find_one(host_name=member_name)
            if member is None:
                raise click.ClickException(f"No member found with host_name '{member_name}'.")
            ref = member.ref
            svc_list = list(services) if services else None
            result = await client.grid.member.restart_services(
                ref,
                services=svc_list,
                restart_option=restart_option,
            )
            svc_label = ", ".join(services) if services else "ALL"
            click.echo(f"Restarted services [{svc_label}] on member '{member_name}' ({ref})")
            if result:
                click.echo(f"  Result: {result}")

    asyncio.run(run())


@cli.command("list-restart-status")
@_shared_options
def list_restart_status(grid_url, username, password, wapi_ver, verify):
    """Show current service restart status across Grid members."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(
                f"{'Member':<35} {'DHCP Status':<18} {'DNS Status':<18} {'Reporting Status'}"
            )
            click.echo("-" * 100)
            async for s in client.grid.restartservicestatus.list():
                click.echo(
                    f"{(s.member or ''):<35} "
                    f"{(s.dhcp_status or ''):<18} "
                    f"{(s.dns_status or ''):<18} "
                    f"{s.reporting_status or ''}"
                )
                count += 1
            if count == 0:
                click.echo("No restart status records found.")
            else:
                click.echo(f"\nTotal: {count}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
