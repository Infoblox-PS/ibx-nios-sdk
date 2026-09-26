# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS admin users, groups, roles, permissions, and auth policy.

Create and list admin users, manage admin groups and roles, audit permissions,
and read/update the grid authentication policy via the ibx-nios-sdk WAPI client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables:
    NIOS_GRID_URL      - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME      - Admin username
    NIOS_PASSWORD      - Admin password
    NIOS_WAPI_VERSION  - Optional; default 2.14

Examples:
    # List all admin users
    python manage_admin_users.py list-users

    # Create an admin user assigned to two groups
    python manage_admin_users.py create-user --new-username alice --new-password s3cr3t --groups read-only dns-admins

    # List admin groups
    python manage_admin_users.py list-groups

    # Create an admin group with roles
    python manage_admin_users.py create-group --name dns-admins --roles dns-editor

    # List admin roles
    python manage_admin_users.py list-roles

    # List permissions (read-only audit)
    python manage_admin_users.py list-permissions

    # Show the current authentication policy
    python manage_admin_users.py get-authpolicy

    # Update the auth policy default group and service order
    python manage_admin_users.py update-authpolicy --default-group read-only --auth-services localuser:authservice/ZG5z...
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
    """Manage NIOS admin users, groups, roles, permissions, and auth policy."""


@cli.command("list-users")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on admin username.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_users(grid_url, username, password, wapi_ver, verify, name_like, json_output):
    """List admin users with username and group memberships."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            if json_output:
                rows = [u async for u in client.security.adminuser.list(**filters)]
                _dump_json(rows)
                return
            count = 0
            click.echo(f"{'Username':<25} {'Groups':<40} {'Comment'}")
            click.echo("-" * 90)
            async for u in client.security.adminuser.list(**filters):
                groups = ", ".join(u.admin_groups or []) if u.admin_groups else ""
                click.echo(f"{(u.name or ''):<25} {groups[:39]:<40} {u.comment or ''}")
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-user")
@_shared_options
@click.option(
    "--new-username", "new_username", required=True, help="Login name for the new admin user."
)
@click.option(
    "--new-password",
    "new_password",
    required=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password for the new admin user.",
)
@click.option(
    "--groups",
    multiple=True,
    metavar="GROUP",
    help="Admin group names to assign the user to (repeatable).",
)
@click.option("--comment", default=None, help="Optional comment.")
@click.option(
    "--disable/--enable", default=False, show_default=True, help="Create user in disabled state."
)
def create_user(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    new_username,
    new_password,
    groups,
    comment,
    disable,
):
    """Create a new NIOS admin user."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload: dict = {
                "name": new_username,
                "password": new_password,
            }
            if groups:
                payload["admin_groups"] = list(groups)
            if comment:
                payload["comment"] = comment
            if disable:
                payload["disable"] = True
            u = await client.security.adminuser.create(payload)
            click.echo(f"Created admin user: {u.name}")
            click.echo(f"  ref:    {u.ref}")
            if u.admin_groups:
                click.echo(f"  groups: {', '.join(u.admin_groups)}")

    asyncio.run(run())


@cli.command("delete-user")
@_shared_options
@click.argument("ref")
def delete_user(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an admin user by WAPI reference.

    \b
    REF - WAPI object reference (e.g. adminuser/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.security.adminuser.delete(ref)
            click.echo(f"Deleted user: {ref}")

    asyncio.run(run())


@cli.command("list-groups")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on group name.")
def list_groups(grid_url, username, password, wapi_ver, verify, name_like):
    """List admin groups."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Group Name':<30} {'Comment'}")
            click.echo("-" * 60)
            async for g in client.security.admingroup.list(**filters):
                click.echo(f"{(g.name or ''):<30} {g.comment or ''}")
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-group")
@_shared_options
@click.option("--name", required=True, help="Name of the new admin group.")
@click.option(
    "--roles", multiple=True, metavar="ROLE", help="Admin role names to assign (repeatable)."
)
@click.option("--comment", default=None, help="Optional comment.")
def create_group(grid_url, username, password, wapi_ver, verify, name, roles, comment):
    """Create a new admin group with optional role assignments."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload: dict = {"name": name}
            if roles:
                payload["roles"] = list(roles)
            if comment:
                payload["comment"] = comment
            g = await client.security.admingroup.create(payload)
            click.echo(f"Created admin group: {g.name}")
            click.echo(f"  ref: {g.ref}")

    asyncio.run(run())


@cli.command("delete-group")
@_shared_options
@click.argument("ref")
def delete_group(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an admin group by WAPI reference.

    \b
    REF - WAPI object reference (e.g. admingroup/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.security.admingroup.delete(ref)
            click.echo(f"Deleted group: {ref}")

    asyncio.run(run())


@cli.command("list-roles")
@_shared_options
def list_roles(grid_url, username, password, wapi_ver, verify):
    """List admin roles."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Role Name':<30} {'Comment'}")
            click.echo("-" * 60)
            async for r in client.security.adminrole.list():
                click.echo(f"{(r.name or ''):<30} {r.comment or ''}")
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("list-permissions")
@_shared_options
@click.option("--group", default=None, help="Filter by admin group name.")
def list_permissions(grid_url, username, password, wapi_ver, verify, group):
    """List permissions (read-only audit view)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if group:
                filters["group"] = group
            count = 0
            click.echo(f"{'Permission':<18} {'Resource Type':<25} {'Group':<25} {'Object'}")
            click.echo("-" * 90)
            async for p in client.security.permission.list(**filters):
                click.echo(
                    f"{(p.permission or ''):<18} "
                    f"{(p.resource_type or ''):<25} "
                    f"{(p.group or ''):<25} "
                    f"{p.object or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("get-authpolicy")
@_shared_options
def get_authpolicy(grid_url, username, password, wapi_ver, verify):
    """Display the current grid authentication policy (singleton)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            policies = await client.security.authpolicy.list().all()
            if not policies:
                raise click.ClickException("No auth policy object found.")
            p = policies[0]
            click.echo(f"  ref:           {p.ref}")
            click.echo(f"  default_group: {p.default_group or 'N/A'}")
            svcs = getattr(p, "auth_services", None) or []
            if svcs:
                click.echo("  auth_services:")
                for svc in svcs:
                    click.echo(f"    - {svc}")
            else:
                click.echo("  auth_services: (none)")

    asyncio.run(run())


@cli.command("update-authpolicy")
@_shared_options
@click.option("--default-group", default=None, help="Name of the default admin group.")
@click.option(
    "--auth-services",
    multiple=True,
    metavar="SERVICE_REF",
    help="Ordered list of auth service WAPI refs (repeatable, in priority order).",
)
def update_authpolicy(
    grid_url, username, password, wapi_ver, verify, default_group, auth_services
):
    """Update the grid authentication policy default group and/or service order."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            policies = await client.security.authpolicy.list().all()
            if not policies:
                raise click.ClickException("No auth policy object found.")
            ref = policies[0].ref
            updates: dict = {}
            if default_group:
                updates["default_group"] = default_group
            if auth_services:
                updates["auth_services"] = list(auth_services)
            if not updates:
                raise click.ClickException(
                    "Provide at least one field to update (--default-group, --auth-services)."
                )
            p = await client.security.authpolicy.update(ref, updates)
            click.echo(f"Updated auth policy: {ref}")
            click.echo(f"  default_group: {p.default_group or 'N/A'}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
