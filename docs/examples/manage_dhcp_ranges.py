# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS DHCP ranges and fixed addresses (IPv4 and IPv6).

List, create, and delete DHCP ranges and fixed addresses. Also supports
querying the next available IP within a DHCP range.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # List all DHCP ranges
    python manage_dhcp_ranges.py list-ranges

    # List ranges in a specific network
    python manage_dhcp_ranges.py list-ranges --network 10.0.0.0/24

    # Create a DHCP range
    python manage_dhcp_ranges.py create-range --network 10.0.0.0/24 \\
        --start-addr 10.0.0.100 --end-addr 10.0.0.200 --comment "Dynamic pool"

    # Get next available IP from a range
    python manage_dhcp_ranges.py range-next-ip range/ZG5z... --num 2

    # List fixed addresses
    python manage_dhcp_ranges.py list-fixed --network 10.0.0.0/24

    # Create a fixed address (MAC reservation)
    python manage_dhcp_ranges.py create-fixed --ipv4addr 10.0.0.50 --mac aa:bb:cc:dd:ee:ff --name printer01

    # Delete a fixed address
    python manage_dhcp_ranges.py delete-fixed fixedaddress/ZG5z...

    # List IPv6 ranges
    python manage_dhcp_ranges.py list-ranges-v6

    # Create an IPv6 fixed address
    python manage_dhcp_ranges.py create-fixed-v6 --ipv6addr 2001:db8::50 --duid 00:01:...
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
    """Manage NIOS DHCP ranges and fixed addresses (IPv4 and IPv6)."""


# ---------------------------------------------------------------------------
# IPv4 ranges
# ---------------------------------------------------------------------------


@cli.command("list-ranges")
@_shared_options
@click.option("--network", default=None, help="Filter by network CIDR (e.g. 10.0.0.0/24).")
@click.option("--network-view", default=None, help="Filter by network view name.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_ranges_cmd(
    grid_url, username, password, wapi_ver, verify, network, network_view, json_output
):
    """List IPv4 DHCP ranges."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view
            if json_output:
                rows = [r async for r in client.dhcp.range.list(**filters)]
                _dump_json(rows)
                return
            count = 0
            click.echo(
                f"{'Start':<18} {'End':<18} {'Network':<20} {'NView':<12} {'Dis':<5} {'Comment'}"
            )
            click.echo("-" * 100)
            async for r in client.dhcp.range.list(**filters):
                click.echo(
                    f"{(r.start_addr or ''):<18} "
                    f"{(r.end_addr or ''):<18} "
                    f"{(r.network or '')[:19]:<20} "
                    f"{(r.network_view or 'default'):<12} "
                    f"{str(r.disable or False):<5} "
                    f"{r.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-range")
@_shared_options
@click.option("--network", required=True, help="Parent network CIDR (e.g. 10.0.0.0/24).")
@click.option("--start-addr", required=True, help="First IP address in the range.")
@click.option("--end-addr", required=True, help="Last IP address in the range.")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_range_cmd(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    network,
    start_addr,
    end_addr,
    network_view,
    comment,
):
    """Create a DHCP IPv4 range."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "network": network,
                "start_addr": start_addr,
                "end_addr": end_addr,
            }
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            r = await client.dhcp.range.create(payload)
            click.echo(f"Created DHCP range: {r.start_addr} - {r.end_addr}")
            click.echo(f"  ref:     {r.ref}")
            click.echo(f"  network: {r.network}")

    asyncio.run(run())


@cli.command("range-next-ip")
@_shared_options
@click.argument("range_ref")
@click.option(
    "--num", default=1, type=int, show_default=True, help="Number of IPs to return from the range."
)
@click.option("--exclude", multiple=True, help="IP address(es) to exclude - repeat for multiple.")
def range_next_ip_cmd(grid_url, username, password, wapi_ver, verify, range_ref, num, exclude):
    """Get the next available IP address(es) from a DHCP range.

    \b
    RANGE_REF - WAPI object reference of the DHCP range (e.g. range/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            kwargs = {"num": num}
            if exclude:
                kwargs["exclude"] = list(exclude)
            result = await client.dhcp.range.next_available_ip(range_ref, **kwargs)
            ips = result.get("ips", [])
            if not ips:
                click.echo("No available IPs found in this range.")
                return
            click.echo(f"Next available IP(s) in range {range_ref}:")
            for ip in ips:
                click.echo(f"  {ip}")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# IPv4 fixed addresses
# ---------------------------------------------------------------------------


@cli.command("list-fixed")
@_shared_options
@click.option("--network", default=None, help="Filter by parent network CIDR.")
@click.option("--network-view", default=None, help="Filter by network view name.")
def list_fixed_cmd(grid_url, username, password, wapi_ver, verify, network, network_view):
    """List IPv4 fixed addresses."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view
            count = 0
            click.echo(f"{'IPv4':<18} {'MAC':<20} {'Name':<25} {'NView':<12} {'Comment'}")
            click.echo("-" * 100)
            async for f in client.dhcp.fixedaddress.list(**filters):
                click.echo(
                    f"{(f.ipv4addr or ''):<18} "
                    f"{(f.mac or ''):<20} "
                    f"{(f.name or '')[:24]:<25} "
                    f"{(f.network_view or 'default'):<12} "
                    f"{f.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-fixed")
@_shared_options
@click.option("--ipv4addr", required=True, help="IPv4 address to reserve.")
@click.option("--mac", required=True, help="MAC address of the client (e.g. aa:bb:cc:dd:ee:ff).")
@click.option("--name", default=None, help="Optional hostname/label for this reservation.")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_fixed_cmd(
    grid_url, username, password, wapi_ver, verify, ipv4addr, mac, name, network_view, comment
):
    """Create an IPv4 fixed address (DHCP MAC reservation)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"ipv4addr": ipv4addr, "mac": mac}
            if name:
                payload["name"] = name
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            f = await client.dhcp.fixedaddress.create(payload)
            click.echo(f"Created fixed address: {f.ipv4addr} -> {f.mac}")
            click.echo(f"  ref:  {f.ref}")
            click.echo(f"  name: {f.name or ''}")

    asyncio.run(run())


@cli.command("delete-range")
@_shared_options
@click.argument("ref")
def delete_range_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a DHCP range by ref.

    \b
    REF - WAPI object reference (e.g. range/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dhcp.range.delete(ref)
            click.echo(f"Deleted range: {ref}")

    asyncio.run(run())


@cli.command("delete-fixed")
@_shared_options
@click.argument("ref")
def delete_fixed_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an IPv4 fixed address.

    \b
    REF - WAPI object reference (e.g. fixedaddress/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dhcp.fixedaddress.delete(ref)
            click.echo(f"Deleted fixed address: {ref}")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# IPv6 ranges
# ---------------------------------------------------------------------------


@cli.command("list-ranges-v6")
@_shared_options
@click.option("--network", default=None, help="Filter by IPv6 network CIDR.")
@click.option("--network-view", default=None, help="Filter by network view name.")
def list_ranges_v6_cmd(grid_url, username, password, wapi_ver, verify, network, network_view):
    """List IPv6 DHCP ranges."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view
            count = 0
            click.echo(f"{'Start':<40} {'End':<40} {'NView':<12} {'Comment'}")
            click.echo("-" * 110)
            async for r in client.dhcp.ipv6range.list(**filters):
                click.echo(
                    f"{(r.start_addr or '')[:39]:<40} "
                    f"{(r.end_addr or '')[:39]:<40} "
                    f"{(r.network_view or 'default'):<12} "
                    f"{r.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-range-v6")
@_shared_options
@click.option("--network", required=True, help="Parent IPv6 network CIDR.")
@click.option("--start-addr", required=True, help="First IPv6 address in the range.")
@click.option("--end-addr", required=True, help="Last IPv6 address in the range.")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_range_v6_cmd(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    network,
    start_addr,
    end_addr,
    network_view,
    comment,
):
    """Create a DHCPv6 range."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "network": network,
                "start_addr": start_addr,
                "end_addr": end_addr,
            }
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            r = await client.dhcp.ipv6range.create(payload)
            click.echo(f"Created DHCPv6 range: {r.start_addr} - {r.end_addr}")
            click.echo(f"  ref: {r.ref}")

    asyncio.run(run())


@cli.command("list-fixed-v6")
@_shared_options
@click.option("--network-view", default=None, help="Filter by network view name.")
def list_fixed_v6_cmd(grid_url, username, password, wapi_ver, verify, network_view):
    """List IPv6 fixed addresses."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network_view:
                filters["network_view"] = network_view
            count = 0
            click.echo(f"{'IPv6':<42} {'DUID':<30} {'Name':<25} {'Comment'}")
            click.echo("-" * 110)
            async for f in client.dhcp.ipv6fixedaddress.list(**filters):
                click.echo(
                    f"{(f.ipv6addr or '')[:41]:<42} "
                    f"{(f.duid or '')[:29]:<30} "
                    f"{(f.name or '')[:24]:<25} "
                    f"{f.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-fixed-v6")
@_shared_options
@click.option("--ipv6addr", required=True, help="IPv6 address to reserve.")
@click.option("--duid", required=True, help="DHCP Unique Identifier (DUID) of the client.")
@click.option("--name", default=None, help="Optional hostname/label for this reservation.")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_fixed_v6_cmd(
    grid_url, username, password, wapi_ver, verify, ipv6addr, duid, name, network_view, comment
):
    """Create an IPv6 fixed address (DHCPv6 reservation)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"ipv6addr": ipv6addr, "duid": duid}
            if name:
                payload["name"] = name
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            f = await client.dhcp.ipv6fixedaddress.create(payload)
            click.echo(f"Created IPv6 fixed address: {f.ipv6addr}")
            click.echo(f"  ref:  {f.ref}")
            click.echo(f"  duid: {f.duid}")
            click.echo(f"  name: {f.name or ''}")

    asyncio.run(run())


@cli.command("delete-range-v6")
@_shared_options
@click.argument("ref")
def delete_range_v6_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an IPv6 DHCP range by ref.

    \b
    REF - WAPI object reference (e.g. ipv6range/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dhcp.ipv6range.delete(ref)
            click.echo(f"Deleted IPv6 range: {ref}")

    asyncio.run(run())


@cli.command("delete-fixed-v6")
@_shared_options
@click.argument("ref")
def delete_fixed_v6_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an IPv6 fixed address.

    \b
    REF - WAPI object reference (e.g. ipv6fixedaddress/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.dhcp.ipv6fixedaddress.delete(ref)
            click.echo(f"Deleted IPv6 fixed address: {ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
