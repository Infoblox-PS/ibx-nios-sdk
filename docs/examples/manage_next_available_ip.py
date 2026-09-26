# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Comprehensive next-available-IP and next-available-network workflows.

Query which IP addresses or network blocks are available within a given NIOS
network or container, and optionally allocate a host record at the next
available IP.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # Get next available IP(s) from an IPv4 network ref
    python manage_next_available_ip.py next-ip network/ZG5z... --num 3

    # Get next available IP excluding specific addresses
    python manage_next_available_ip.py next-ip network/ZG5z... --exclude 10.0.0.1 --exclude 10.0.0.2

    # Get next available /24 from a network container
    python manage_next_available_ip.py next-network networkcontainer/ZG5z... --cidr 24

    # Carve 3 /26 subnets from a container, excluding one block
    python manage_next_available_ip.py next-network networkcontainer/ZG5z... --cidr 26 --num 3

    # Find next available IP in a network and create an A record for a hostname
    python manage_next_available_ip.py allocate-host \\
        --network-ref network/ZG5z... \\
        --hostname web01.example.com \\
        --view default
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
    """Next-available-IP and next-available-network IPAM workflows."""


@cli.command("next-ip")
@_shared_options
@click.argument("network_ref")
@click.option(
    "--num", default=1, type=int, show_default=True, help="Number of IP addresses to return."
)
@click.option(
    "--exclude",
    multiple=True,
    help="IP address(es) to exclude - repeat for multiple: --exclude 10.0.0.1 --exclude 10.0.0.2",
)
def next_ip_cmd(grid_url, username, password, wapi_ver, verify, network_ref, num, exclude):
    """Return the next available IP address(es) within a network.

    Supports both IPv4 networks (network/...) and IPv6 networks (ipv6network/...).

    \b
    NETWORK_REF - WAPI object reference of the network
                  (e.g. network/ZG5z... or ipv6network/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            rtype = network_ref.split("/")[0]
            if rtype == "network":
                resource = client.ipam.network
            elif rtype == "ipv6network":
                resource = client.ipam.ipv6network
            else:
                raise click.ClickException(
                    f"Unsupported ref type '{rtype}'. Expected 'network' or 'ipv6network'."
                )

            kwargs = {"num": num}
            if exclude:
                kwargs["exclude"] = list(exclude)

            result = await resource.next_available_ip(network_ref, **kwargs)
            ips = result.get("ips", [])
            if not ips:
                click.echo("No available IPs found in this network.")
                return
            click.echo(f"Next available IP(s) in {network_ref}:")
            for ip in ips:
                click.echo(f"  {ip}")

    asyncio.run(run())


@cli.command("next-network")
@_shared_options
@click.argument("container_ref")
@click.option(
    "--cidr",
    required=True,
    type=int,
    help="Prefix length for the carved-out network (e.g. 24 for /24).",
)
@click.option(
    "--num", default=1, type=int, show_default=True, help="Number of networks to return."
)
@click.option("--exclude", multiple=True, help="Network CIDR(s) to exclude - repeat for multiple.")
def next_network_cmd(
    grid_url, username, password, wapi_ver, verify, container_ref, cidr, num, exclude
):
    """Return the next available sub-network(s) within a network container.

    Supports IPv4 containers (networkcontainer/...) and IPv6 containers
    (ipv6networkcontainer/...).

    \b
    CONTAINER_REF - WAPI object reference of the network container
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            rtype = container_ref.split("/")[0]
            if rtype == "networkcontainer":
                resource = client.ipam.networkcontainer
            elif rtype == "ipv6networkcontainer":
                resource = client.ipam.ipv6networkcontainer
            else:
                raise click.ClickException(
                    f"Unsupported ref type '{rtype}'. Expected 'networkcontainer' or 'ipv6networkcontainer'."
                )

            kwargs = {"cidr": cidr, "num": num}
            if exclude:
                kwargs["exclude"] = list(exclude)

            result = await resource.next_available_network(container_ref, **kwargs)
            networks = result.get("networks", [])
            if not networks:
                click.echo("No available networks found in this container.")
                return
            click.echo(f"Next available /{cidr} network(s) in {container_ref}:")
            for net in networks:
                click.echo(f"  {net}")

    asyncio.run(run())


@cli.command("allocate-host")
@_shared_options
@click.option(
    "--network-ref",
    required=True,
    help="WAPI ref of the IPv4 network to allocate from (e.g. network/ZG5z...).",
)
@click.option("--hostname", required=True, help="Fully-qualified hostname for the A record.")
@click.option(
    "--view", default=None, help="DNS view to create the A record in (omit for grid default)."
)
@click.option("--comment", default=None, help="Optional comment for the A record.")
def allocate_host_cmd(
    grid_url, username, password, wapi_ver, verify, network_ref, hostname, view, comment
):
    """Find the next available IP in a network and register an A record for a hostname.

    This command:
      1. Queries next_available_ip on the network.
      2. Creates a DNS A record pointing the hostname to that IP.
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # Step 1: get next available IP
            click.echo(f"Querying next available IP in: {network_ref}")
            result = await client.ipam.network.next_available_ip(network_ref, num=1)
            ips = result.get("ips", [])
            if not ips:
                raise click.ClickException("No available IPs found in this network.")
            ip = ips[0]
            click.echo(f"Next available IP: {ip}")

            # Step 2: create DNS A record
            payload = {"name": hostname, "ipv4addr": ip}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment

            click.echo(f"Creating A record: {hostname} -> {ip}")
            r = await client.dns.record_a.create(payload)
            click.echo("A record created successfully.")
            click.echo(f"  ref:      {r.ref}")
            click.echo(f"  name:     {r.name}")
            click.echo(f"  ipv4addr: {r.ipv4addr}")
            click.echo(f"  view:     {r.view or 'default'}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
