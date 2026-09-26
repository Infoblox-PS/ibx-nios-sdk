# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS DNS views.

List, create, update, and delete DNS views using the ibx-nios-sdk WAPI client.
DNS views allow a Grid to serve different answers for the same DNS query
depending on the querying client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # List all DNS views
    python manage_dns_views.py list

    # Get a specific view by ref
    python manage_dns_views.py get view/ZG5z...

    # Create a new DNS view
    python manage_dns_views.py create --name internal --comment "Internal view"

    # Update a view's comment
    python manage_dns_views.py update view/ZG5z... --comment "Updated comment"

    # Delete a view
    python manage_dns_views.py delete view/ZG5z...
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
    """Manage NIOS DNS views."""


@cli.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on view name.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_cmd(grid_url, username, password, wapi_ver, verify, name_like, json_output):
    """List DNS views."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            if json_output:
                rows = [v async for v in client.dns.view.list(**filters)]
                _dump_json(rows)
                return
            count = 0
            click.echo(f"{'Name':<25} {'Is Default':<12} {'Disabled':<10} {'Comment'}")
            click.echo("-" * 80)
            async for v in client.dns.view.list(**filters):
                click.echo(
                    f"{(v.name or '')[:24]:<25} "
                    f"{str(getattr(v, 'is_default', False) or False):<12} "
                    f"{str(v.disable or False):<10} "
                    f"{v.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("get")
@_shared_options
@click.argument("ref")
def get_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Get a single DNS view by reference.

    \b
    REF - WAPI object reference (e.g. view/ZG5z...:internal/false)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            v = await client.dns.view.get(ref)
            click.echo(f"  ref:        {v.ref}")
            click.echo(f"  name:       {v.name}")
            click.echo(f"  disable:    {v.disable}")
            click.echo(f"  is_default: {getattr(v, 'is_default', None)}")
            click.echo(f"  comment:    {v.comment or ''}")

    asyncio.run(run())


@cli.command("create")
@_shared_options
@click.option("--name", required=True, help="View name (unique within the Grid).")
@click.option("--comment", default=None, help="Optional comment.")
@click.option(
    "--disable/--enable",
    default=False,
    show_default=True,
    help="Create the view in a disabled state.",
)
def create_cmd(grid_url, username, password, wapi_ver, verify, name, comment, disable):
    """Create a new DNS view."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name}
            if comment:
                payload["comment"] = comment
            if disable:
                payload["disable"] = True
            v = await client.dns.view.create(payload)
            click.echo(f"Created DNS view: {v.name}")
            click.echo(f"  ref:     {v.ref}")
            click.echo(f"  comment: {v.comment or ''}")

    asyncio.run(run())


@cli.command("update")
@_shared_options
@click.argument("ref")
@click.option("--comment", default=None, help="New comment value.")
@click.option("--disable/--enable", default=None, help="Disable or enable the view.")
def update_cmd(grid_url, username, password, wapi_ver, verify, ref, comment, disable):
    """Update a DNS view.

    \b
    REF - WAPI object reference for the view to update
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            updates = {}
            if comment is not None:
                updates["comment"] = comment
            if disable is not None:
                updates["disable"] = disable
            if not updates:
                raise click.ClickException("Provide at least one field to update.")
            v = await client.dns.view.update(ref, updates)
            click.echo(f"Updated DNS view: {v.name}")
            click.echo(f"  ref:     {v.ref}")
            click.echo(f"  comment: {v.comment or ''}")
            click.echo(f"  disable: {v.disable}")

    asyncio.run(run())


@cli.command("delete")
@_shared_options
@click.argument("ref")
def delete_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a DNS view.

    \b
    REF - WAPI object reference for the view to delete
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dns.view.delete(ref)
            click.echo(f"Deleted DNS view: {ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
