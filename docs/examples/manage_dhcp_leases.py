# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Read-only DHCP lease inventory for NIOS.

Browse and filter active DHCP leases across your Grid. Lease objects are
read-only in WAPI; this script provides list and get subcommands only.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # List all active leases
    python manage_dhcp_leases.py list --binding-state ACTIVE

    # List leases in a specific network
    python manage_dhcp_leases.py list --network 10.0.0.0/24

    # Filter by hostname substring
    python manage_dhcp_leases.py list --hostname-like laptop

    # Filter by IP address substring
    python manage_dhcp_leases.py list --address-like 10.0.0

    # Get a single lease by ref
    python manage_dhcp_leases.py get lease/ZG5z...

    # Show lease summary statistics
    python manage_dhcp_leases.py summary --network 10.0.0.0/24
"""

import asyncio
import datetime
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


def _fmt_epoch(ts):
    """Format an epoch timestamp to a human-readable string, or return 'N/A'."""
    if ts is None:
        return "N/A"
    try:
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)


@click.group()
def cli():
    """Read-only DHCP lease inventory."""


@cli.command("list")
@_shared_options
@click.option("--network", default=None, help="Filter by network CIDR (e.g. 10.0.0.0/24).")
@click.option("--network-view", default=None, help="Filter by network view name.")
@click.option(
    "--binding-state",
    default=None,
    type=click.Choice(
        ["ACTIVE", "EXPIRED", "FREE", "RELEASED", "ABANDONED"], case_sensitive=False
    ),
    help="Filter by lease binding state.",
)
@click.option("--address-like", default=None, help="Substring filter on IP address.")
@click.option("--hostname-like", default=None, help="Substring filter on client hostname.")
@click.option(
    "--max-results",
    default=500,
    type=int,
    show_default=True,
    help="Maximum number of leases to return per page.",
)
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_cmd(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    network,
    network_view,
    binding_state,
    address_like,
    hostname_like,
    max_results,
    json_output,
):
    """List DHCP leases (read-only)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view
            if binding_state:
                filters["binding_state"] = binding_state.upper()
            if address_like:
                filters["address__like"] = address_like
            if hostname_like:
                filters["client_hostname__like"] = hostname_like

            if json_output:
                rows = [
                    lease
                    async for lease in client.dhcp.lease.list(
                        max_results=max_results,
                        return_fields_plus=["starts", "ends"],
                        **filters,
                    )
                ]
                _dump_json(rows)
                return

            count = 0
            click.echo(
                f"{'IP Address':<18} "
                f"{'MAC/Hardware':<20} "
                f"{'Hostname':<28} "
                f"{'State':<12} "
                f"{'Starts':<22} "
                f"{'Ends'}"
            )
            click.echo("-" * 120)
            async for lease in client.dhcp.lease.list(
                max_results=max_results,
                return_fields_plus=["starts", "ends"],
                **filters,
            ):
                click.echo(
                    f"{(lease.address or ''):<18} "
                    f"{(lease.hardware or ''):<20} "
                    f"{(lease.client_hostname or '')[:27]:<28} "
                    f"{(lease.binding_state or ''):<12} "
                    f"{_fmt_epoch(lease.starts):<22} "
                    f"{_fmt_epoch(lease.ends)}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("get")
@_shared_options
@click.argument("ref")
def get_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Get full details for a single DHCP lease by reference.

    \b
    REF - WAPI object reference (e.g. lease/ZG5z...:10.0.0.50/default)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            lease = await client.dhcp.lease.get(
                ref,
                return_fields_plus=[
                    "starts",
                    "ends",
                    "protocol",
                    "served_by",
                    "server_host_name",
                    "username",
                    "uid",
                ],
            )
            click.echo(f"  ref:             {lease.ref}")
            click.echo(f"  address:         {lease.address}")
            click.echo(f"  hardware:        {lease.hardware or 'N/A'}")
            click.echo(f"  client_hostname: {lease.client_hostname or 'N/A'}")
            click.echo(f"  binding_state:   {lease.binding_state or 'N/A'}")
            click.echo(f"  network:         {lease.network or 'N/A'}")
            click.echo(f"  network_view:    {lease.network_view or 'N/A'}")
            click.echo(f"  protocol:        {lease.protocol or 'N/A'}")
            click.echo(f"  starts:          {_fmt_epoch(lease.starts)}")
            click.echo(f"  ends:            {_fmt_epoch(lease.ends)}")
            click.echo(f"  served_by:       {lease.served_by or 'N/A'}")
            click.echo(f"  server_hostname: {lease.server_host_name or 'N/A'}")
            click.echo(f"  username:        {lease.username or 'N/A'}")
            click.echo(f"  uid:             {lease.uid or 'N/A'}")

    asyncio.run(run())


@cli.command("summary")
@_shared_options
@click.option("--network", default=None, help="Restrict summary to a specific network CIDR.")
@click.option("--network-view", default=None, help="Filter by network view name.")
def summary_cmd(grid_url, username, password, wapi_ver, verify, network, network_view):
    """Show a count summary of leases grouped by binding state."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view

            state_counts: dict[str, int] = {}
            total = 0
            async for lease in client.dhcp.lease.list(**filters):
                state = lease.binding_state or "UNKNOWN"
                state_counts[state] = state_counts.get(state, 0) + 1
                total += 1

            if network:
                click.echo(f"Lease summary for network: {network}")
            else:
                click.echo("Lease summary (all networks):")
            click.echo(f"{'State':<15} {'Count':>8}")
            click.echo("-" * 25)
            for state in sorted(state_counts):
                click.echo(f"{state:<15} {state_counts[state]:>8}")
            click.echo("-" * 25)
            click.echo(f"{'TOTAL':<15} {total:>8}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
