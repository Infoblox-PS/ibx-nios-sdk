# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS DTC (Dynamic Traffic Control) pools.

Full CRUD lifecycle for DTC pool objects, including member server assignment
and health monitor attachment. Pools group DTC servers and define the
load-balancing strategy for a set of endpoints.

In the NIOS WAPI, a pool's ``servers`` field is a list of dicts with the shape:
    {"server": "<dtc:server ref>", "ratio": <int>}

The ``monitors`` field is a list of bare object reference strings:
    ["<dtc:monitor:http ref>", ...]
(WAPI auto-detects the monitor type from the ref prefix; sending dicts with
``monitor_type`` causes an "Object reference expected" error.)

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as defaults):
    NIOS_GRID_URL      - Grid URL, e.g. https://192.168.1.2
    NIOS_USERNAME      - WAPI username
    NIOS_PASSWORD      - WAPI password
    NIOS_WAPI_VERSION  - WAPI version (default: 2.14)

Example usage:

    # List all pools
    python manage_dtc_pools.py list

    # Create a pool with ROUND_ROBIN load balancing
    python manage_dtc_pools.py create --name app-pool --lb-preferred-method ROUND_ROBIN

    # Add a server member with ratio 1
    python manage_dtc_pools.py add-member dtc:pool/ZG5z... dtc:server/ZG5z...

    # Attach an HTTP monitor
    python manage_dtc_pools.py create --name app-pool \\
        --monitors dtc:monitor:http/ZG5z...

    # Remove a server member
    python manage_dtc_pools.py remove-member dtc:pool/ZG5z... dtc:server/ZG5z...

    # Delete a pool (prompts for confirmation)
    python manage_dtc_pools.py delete dtc:pool/ZG5z...
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
    """Manage NIOS DTC pool objects (dtc:pool).

    Pools define a set of servers and the load-balancing policy that governs
    how traffic is distributed across them. Each pool can attach one or more
    health monitors and be referenced by an LBDN.

    Server membership is encoded as a list of dicts:
        [{"server": "<ref>", "ratio": 1}, ...]

    Monitor attachment uses bare ref strings:
        ["<dtc:monitor:* ref>", ...]
    """


@cli.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Filter pools whose name contains this string.")
def cmd_list(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name_like: str | None,
) -> None:
    """List DTC pools, optionally filtered by name substring."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like

            pools = await client.dtc.pool.list(**filters).all()

            if not pools:
                click.echo("No DTC pools found.")
                return

            click.echo(f"{'Name':<28} {'LB Method':<20} {'Servers':<9} {'Comment'}")
            click.echo("-" * 80)
            for p in pools:
                srv_count = len(p.servers or [])
                click.echo(
                    f"{p.name or '':<28} "
                    f"{p.lb_preferred_method or '':<20} "
                    f"{srv_count:<9} "
                    f"{p.comment or ''}"
                )
            click.echo(f"\nTotal: {len(pools)} pool(s)")

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
    """Get full details of a DTC pool by its WAPI reference (REF).

    REF is the WAPI object reference, e.g. dtc:pool/ZG5z...:app-pool
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            pool = await client.dtc.pool.get(
                ref,
                return_fields_plus=[
                    "servers",
                    "monitors",
                    "disable",
                    "availability",
                    "ttl",
                    "health",
                    "lb_preferred_topology",
                    "lb_alternate_method",
                ],
            )
            click.echo(f"  ref:                  {pool.ref}")
            click.echo(f"  name:                 {pool.name}")
            click.echo(f"  lb_preferred_method:  {pool.lb_preferred_method}")
            click.echo(f"  availability:         {pool.availability}")
            click.echo(f"  disable:              {pool.disable}")
            click.echo(f"  comment:              {pool.comment}")
            if pool.servers:
                click.echo(f"  servers ({len(pool.servers)}):")
                for entry in pool.servers:
                    click.echo(f"    server={entry.get('server')}  ratio={entry.get('ratio', 1)}")
            if pool.monitors:
                click.echo(f"  monitors ({len(pool.monitors)}):")
                for entry in pool.monitors:
                    click.echo(
                        f"    monitor={entry.get('monitor')}  type={entry.get('monitor_type')}"
                    )
            if pool.health:
                click.echo(f"  health: {pool.health}")

    asyncio.run(run())


@cli.command("create")
@_shared_options
@click.option("--name", required=True, help="Display name for the pool.")
@click.option("--comment", default=None, help="Optional comment (max 256 chars).")
@click.option(
    "--preferred-topology",
    default=None,
    help="WAPI ref of a dtc:topology object to use for topology-based LB.",
)
@click.option(
    "--lb-preferred-method",
    default="ROUND_ROBIN",
    show_default=True,
    type=click.Choice(
        ["ROUND_ROBIN", "RATIO", "GLOBAL_AVAILABILITY", "TOPOLOGY", "DYNAMIC_RATIO"],
        case_sensitive=False,
    ),
    help="Preferred load-balancing method.",
)
@click.option(
    "--monitors",
    multiple=True,
    help="WAPI ref(s) of monitor objects to attach (repeatable). "
    "The monitor type is inferred from the ref prefix.",
)
def cmd_create(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    comment: str | None,
    preferred_topology: str | None,
    lb_preferred_method: str,
    monitors: tuple[str, ...],
) -> None:
    """Create a new DTC pool.

    Monitors can be attached at creation time with ``--monitors``.  To add
    server members after creation use the ``add-member`` subcommand.
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {
                "name": name,
                "lb_preferred_method": lb_preferred_method.upper(),
            }
            if comment:
                body["comment"] = comment
            if preferred_topology:
                body["lb_preferred_topology"] = preferred_topology
            if monitors:
                # WAPI expects bare ref strings; monitor_type is auto-detected from prefix
                body["monitors"] = list(monitors)

            pool = await client.dtc.pool.create(
                body,
                return_fields_plus=[
                    "servers",
                    "monitors",
                    "lb_preferred_method",
                    "availability",
                ],
            )
            click.secho("  [OK] DTC pool created", fg="green")
            click.echo(f"  ref:                 {pool.ref}")
            click.echo(f"  name:                {pool.name}")
            click.echo(f"  lb_preferred_method: {pool.lb_preferred_method}")
            click.echo(f"  monitors attached:   {len(pool.monitors or [])}")

    asyncio.run(run())


@cli.command("add-member")
@_shared_options
@click.argument("pool_ref")
@click.argument("server_ref")
@click.option(
    "--ratio",
    default=1,
    type=int,
    show_default=True,
    help="Load-balancing weight for this server member.",
)
def cmd_add_member(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    pool_ref: str,
    server_ref: str,
    ratio: int,
) -> None:
    """Add a server as a member of a pool (POOL_REF SERVER_REF).

    POOL_REF   - WAPI ref of the target pool, e.g. dtc:pool/ZG5z...
    SERVER_REF - WAPI ref of the server to add, e.g. dtc:server/ZG5z...

    The existing servers list is fetched, the new entry is appended, then
    a PUT is issued with the full updated list.  Duplicate refs are skipped.
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # Fetch current pool state so we can merge the server list
            pool = await client.dtc.pool.get(pool_ref, return_fields_plus=["servers"])
            current_servers: list[dict] = list(pool.servers or [])

            # Prevent duplicates
            existing_refs = {entry.get("server") for entry in current_servers}
            if server_ref in existing_refs:
                click.echo(f"  Server '{server_ref}' is already a member of this pool. No change.")
                return

            current_servers.append({"server": server_ref, "ratio": ratio})

            updated = await client.dtc.pool.update(
                pool_ref,
                {"servers": current_servers},
                return_fields_plus=["servers"],
            )
            click.secho("  [OK] Member added", fg="green")
            click.echo(f"  pool:    {pool_ref}")
            click.echo(f"  servers: {len(updated.servers or [])} total member(s)")
            for entry in updated.servers or []:
                click.echo(f"    server={entry.get('server')}  ratio={entry.get('ratio', 1)}")

    asyncio.run(run())


@cli.command("remove-member")
@_shared_options
@click.argument("pool_ref")
@click.argument("server_ref")
def cmd_remove_member(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    pool_ref: str,
    server_ref: str,
) -> None:
    """Remove a server from a pool's member list (POOL_REF SERVER_REF).

    POOL_REF   - WAPI ref of the target pool, e.g. dtc:pool/ZG5z...
    SERVER_REF - WAPI ref of the server to remove, e.g. dtc:server/ZG5z...

    The pool's servers list is fetched, the matching entry removed, then PUT.
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            pool = await client.dtc.pool.get(pool_ref, return_fields_plus=["servers"])
            current_servers: list[dict] = list(pool.servers or [])
            filtered = [entry for entry in current_servers if entry.get("server") != server_ref]

            if len(filtered) == len(current_servers):
                click.echo(f"  Server '{server_ref}' is not a member of this pool. No change.")
                return

            updated = await client.dtc.pool.update(
                pool_ref,
                {"servers": filtered},
                return_fields_plus=["servers"],
            )
            click.secho("  [OK] Member removed", fg="green")
            click.echo(f"  pool:    {pool_ref}")
            click.echo(f"  servers: {len(updated.servers or [])} remaining member(s)")

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
    """Delete a DTC pool by WAPI reference (REF).

    REF is the WAPI object reference, e.g. dtc:pool/ZG5z...:app-pool.
    You will be prompted to confirm before deletion.
    """

    async def run() -> None:
        click.confirm(f"Delete DTC pool '{ref}'?", abort=True)
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            deleted = await client.dtc.pool.delete(ref)
            click.secho(f"  [OK] Deleted: {deleted}", fg="green")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
