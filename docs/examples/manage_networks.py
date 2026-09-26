# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS IPAM networks and network containers (IPv4 and IPv6).

List, create, and delete IPv4/IPv6 networks and network containers using the
ibx-nios-sdk WAPI client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # List all IPv4 networks
    python manage_networks.py list-v4

    # List IPv4 networks in a specific network view
    python manage_networks.py list-v4 --network-view default

    # List IPv6 networks
    python manage_networks.py list-v6

    # Create an IPv4 network
    python manage_networks.py create-v4 --network 10.0.0.0/24 --comment "Prod LAN"

    # Create an IPv6 network
    python manage_networks.py create-v6 --network 2001:db8::/32 --network-view default

    # Create an IPv4 network container
    python manage_networks.py create-container-v4 --network 10.0.0.0/8 --comment "Top-level container"

    # Create an IPv6 network container
    python manage_networks.py create-container-v6 --network 2001:db8::/32

    # Delete any network or container by ref
    python manage_networks.py delete network/ZG5z...
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


def _print_network_table(networks):
    click.echo(f"{'Network':<22} {'Network View':<18} {'Disabled':<10} {'Comment'}")
    click.echo("-" * 80)
    count = 0
    for n in networks:
        click.echo(
            f"{(n.network or '')[:21]:<22} "
            f"{(n.network_view or 'default'):<18} "
            f"{str(n.disable or False):<10} "
            f"{n.comment or ''}"
        )
        count += 1
    return count


@click.group()
def cli():
    """Manage NIOS IPAM networks and network containers (IPv4 and IPv6)."""


@cli.command("list-v4")
@_shared_options
@click.option("--network", default=None, help="Filter by exact network CIDR (e.g. 10.0.0.0/8).")
@click.option("--network-view", default=None, help="Filter by network view name.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_v4_cmd(
    grid_url, username, password, wapi_ver, verify, network, network_view, json_output
):
    """List IPv4 networks."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view
            rows = []
            async for n in client.ipam.network.list(**filters):
                rows.append(n)
            if json_output:
                _dump_json(rows)
                return
            count = _print_network_table(rows)
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("list-v6")
@_shared_options
@click.option("--network", default=None, help="Filter by exact IPv6 network CIDR.")
@click.option("--network-view", default=None, help="Filter by network view name.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_v6_cmd(
    grid_url, username, password, wapi_ver, verify, network, network_view, json_output
):
    """List IPv6 networks."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network:
                filters["network"] = network
            if network_view:
                filters["network_view"] = network_view
            rows = []
            async for n in client.ipam.ipv6network.list(**filters):
                rows.append(n)
            if json_output:
                _dump_json(rows)
                return
            count = _print_network_table(rows)
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("list-containers-v4")
@_shared_options
@click.option("--network-view", default=None, help="Filter by network view name.")
def list_containers_v4_cmd(grid_url, username, password, wapi_ver, verify, network_view):
    """List IPv4 network containers."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network_view:
                filters["network_view"] = network_view
            rows = []
            async for n in client.ipam.networkcontainer.list(**filters):
                rows.append(n)
            count = _print_network_table(rows)
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("list-containers-v6")
@_shared_options
@click.option("--network-view", default=None, help="Filter by network view name.")
def list_containers_v6_cmd(grid_url, username, password, wapi_ver, verify, network_view):
    """List IPv6 network containers."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if network_view:
                filters["network_view"] = network_view
            rows = []
            async for n in client.ipam.ipv6networkcontainer.list(**filters):
                rows.append(n)
            count = _print_network_table(rows)
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-v4")
@_shared_options
@click.option("--network", required=True, help="IPv4 CIDR (e.g. 192.168.1.0/24).")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_v4_cmd(grid_url, username, password, wapi_ver, verify, network, network_view, comment):
    """Create an IPv4 network."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"network": network}
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            n = await client.ipam.network.create(payload)
            click.echo(f"Created IPv4 network: {n.network}")
            click.echo(f"  ref:          {n.ref}")
            click.echo(f"  network_view: {n.network_view or 'default'}")

    asyncio.run(run())


@cli.command("create-v6")
@_shared_options
@click.option("--network", required=True, help="IPv6 CIDR (e.g. 2001:db8::/48).")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_v6_cmd(grid_url, username, password, wapi_ver, verify, network, network_view, comment):
    """Create an IPv6 network."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"network": network}
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            n = await client.ipam.ipv6network.create(payload)
            click.echo(f"Created IPv6 network: {n.network}")
            click.echo(f"  ref:          {n.ref}")
            click.echo(f"  network_view: {n.network_view or 'default'}")

    asyncio.run(run())


@cli.command("create-container-v4")
@_shared_options
@click.option("--network", required=True, help="IPv4 container CIDR (e.g. 10.0.0.0/8).")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_container_v4_cmd(
    grid_url, username, password, wapi_ver, verify, network, network_view, comment
):
    """Create an IPv4 network container."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"network": network}
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            n = await client.ipam.networkcontainer.create(payload)
            click.echo(f"Created IPv4 network container: {n.network}")
            click.echo(f"  ref:          {n.ref}")
            click.echo(f"  network_view: {n.network_view or 'default'}")

    asyncio.run(run())


@cli.command("create-container-v6")
@_shared_options
@click.option("--network", required=True, help="IPv6 container CIDR (e.g. 2001:db8::/32).")
@click.option("--network-view", default=None, help="Network view name (omit for default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_container_v6_cmd(
    grid_url, username, password, wapi_ver, verify, network, network_view, comment
):
    """Create an IPv6 network container."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"network": network}
            if network_view:
                payload["network_view"] = network_view
            if comment:
                payload["comment"] = comment
            n = await client.ipam.ipv6networkcontainer.create(payload)
            click.echo(f"Created IPv6 network container: {n.network}")
            click.echo(f"  ref:          {n.ref}")
            click.echo(f"  network_view: {n.network_view or 'default'}")

    asyncio.run(run())


@cli.command("delete")
@_shared_options
@click.argument("ref")
def delete_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a network or network container by WAPI reference.

    \b
    REF - WAPI object reference (e.g. network/ZG5z..., networkcontainer/ZG5z...,
          ipv6network/ZG5z..., ipv6networkcontainer/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            rtype = ref.split("/")[0]
            resource_map = {
                "network": client.ipam.network,
                "networkcontainer": client.ipam.networkcontainer,
                "ipv6network": client.ipam.ipv6network,
                "ipv6networkcontainer": client.ipam.ipv6networkcontainer,
            }
            resource = resource_map.get(rtype)
            if resource is None:
                raise click.ClickException(
                    f"Unrecognized ref type '{rtype}'. Supported: {list(resource_map)}"
                )
            await resource.delete(ref)
            click.echo(f"Deleted {rtype}: {ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
