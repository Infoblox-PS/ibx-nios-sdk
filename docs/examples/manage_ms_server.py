# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Microsoft Server integrations - AD, DHCP, DNS servers and AD sites.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL        - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME        - Admin username
    NIOS_PASSWORD        - Admin password
    NIOS_WAPI_VERSION    - Optional; default 2.14

Examples:
    # List all Microsoft servers
    python manage_ms_server.py list-servers

    # Get a specific server
    python manage_ms_server.py get "msserver/ZG5z..."

    # Add a Microsoft server
    python manage_ms_server.py add-server \\
        --address 192.168.10.50 \\
        --ad-user "CORP\\SvcNIOS" \\
        --ad-password "P@ssw0rd" \\
        --comment "Primary DC"

    # Remove a Microsoft server
    python manage_ms_server.py remove-server "msserver/ZG5z..."

    # List DNS sub-configurations on a Microsoft server
    python manage_ms_server.py list-dns-on "msserver/ZG5z..."

    # List DHCP sub-configurations on a Microsoft server
    python manage_ms_server.py list-dhcp-on "msserver/ZG5z..."

    # List Active Directory sites
    python manage_ms_server.py list-adsites

    # List Active Directory domains
    python manage_ms_server.py list-domains
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
    """Manage NIOS Microsoft Server integrations - AD, DNS, DHCP servers and AD sites."""


@cli.command("list-servers")
@_shared_options
@click.option("--address-like", default=None, help="Substring filter on server address.")
@click.option("--domain", default=None, help="Filter by AD domain name.")
def list_servers_cmd(grid_url, username, password, wapi_ver, verify, address_like, domain):
    """List Microsoft servers registered with NIOS."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if address_like:
                filters["address__like"] = address_like
            if domain:
                filters["ad_domain"] = domain
            count = 0
            click.echo(
                f"{'Address':<20} {'Domain':<30} {'Conn Status':<15} {'Sync Status':<15} {'Ref'}"
            )
            click.echo("-" * 120)
            async for s in client.microsoftserver.msserver.list(**filters):
                click.echo(
                    f"{(s.address or ''):<20} "
                    f"{(s.ad_domain or '')[:29]:<30} "
                    f"{(s.connection_status or ''):<15} "
                    f"{(s.synchronization_status or ''):<15} "
                    f"{s.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} Microsoft server(s)")

    asyncio.run(run())


@cli.command("get")
@_shared_options
@click.argument("server_ref")
def get_server_cmd(grid_url, username, password, wapi_ver, verify, server_ref):
    """Get details for a Microsoft server by its WAPI reference.

    \b
    SERVER_REF - WAPI object reference (e.g. msserver/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            s = await client.microsoftserver.msserver.get(server_ref)
            click.echo(f"Ref:                   {s.ref}")
            click.echo(f"Address:               {s.address}")
            click.echo(f"AD Domain:             {s.ad_domain}")
            click.echo(f"Connection Status:     {s.connection_status}")
            click.echo(f"Connection Detail:     {s.connection_status_detail}")
            click.echo(f"Sync Status:           {s.synchronization_status}")
            click.echo(f"Sync Detail:           {s.synchronization_status_detail}")
            click.echo(f"Version:               {s.version}")
            click.echo(f"Last Seen:             {s.last_seen}")
            if s.comment:
                click.echo(f"Comment:               {s.comment}")

    asyncio.run(run())


@cli.command("add-server")
@_shared_options
@click.option("--address", required=True, help="IP address or FQDN of the Microsoft server.")
@click.option("--ad-user", required=True, help="Active Directory user (e.g. CORP\\\\SvcNIOS).")
@click.option("--ad-password", required=True, hide_input=True, help="Active Directory password.")
@click.option("--ad-domain", default=None, help="Active Directory domain FQDN.")
@click.option("--comment", default=None, help="Optional comment.")
@click.option(
    "--disable/--enable",
    default=False,
    show_default=True,
    help="Disable synchronization for this server.",
)
def add_server_cmd(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    address,
    ad_user,
    ad_password,
    ad_domain,
    comment,
    disable,
):
    """Add a Microsoft server to NIOS for AD/DHCP/DNS synchronization."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "address": address,
                "ad_user": {"name": ad_user, "password": ad_password},
                "disabled": disable,
            }
            if ad_domain:
                payload["ad_domain"] = ad_domain
            if comment:
                payload["comment"] = comment
            s = await client.microsoftserver.msserver.create(payload)
            click.echo(f"Added Microsoft server: {s.address}")
            click.echo(f"  ad_domain: {s.ad_domain}")
            click.echo(f"  disabled:  {s.disabled}")
            click.echo(f"  ref:       {s.ref}")

    asyncio.run(run())


@cli.command("remove-server")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to remove this Microsoft server?")
def remove_server_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Remove a Microsoft server from NIOS by ref.

    \b
    REF - WAPI object reference (e.g. msserver/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.microsoftserver.msserver.delete(ref)
            click.echo(f"Removed Microsoft server: {ref}")

    asyncio.run(run())


@cli.command("list-dns-on")
@_shared_options
@click.argument("server_ref")
def list_dns_on_cmd(grid_url, username, password, wapi_ver, verify, server_ref):
    """List DNS sub-configurations on a Microsoft server.

    \b
    SERVER_REF - Parent msserver WAPI reference (e.g. msserver/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Address':<20} {'UUID':<40} {'Ref'}")
            click.echo("-" * 100)
            async for d in client.microsoftserver.dns.list(msserver=server_ref):
                click.echo(f"{(d.address or ''):<20} {(d.uuid or ''):<40} {d.ref or ''}")
                count += 1
            click.echo(f"\nTotal: {count} DNS configuration(s)")

    asyncio.run(run())


@cli.command("list-dhcp-on")
@_shared_options
@click.argument("server_ref")
def list_dhcp_on_cmd(grid_url, username, password, wapi_ver, verify, server_ref):
    """List DHCP sub-configurations on a Microsoft server.

    \b
    SERVER_REF - Parent msserver WAPI reference (e.g. msserver/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Address':<20} {'Server Name':<30} {'Status':<15} {'Ref'}")
            click.echo("-" * 100)
            async for d in client.microsoftserver.dhcp.list(msserver=server_ref):
                click.echo(
                    f"{(d.address or ''):<20} "
                    f"{(d.server_name or '')[:29]:<30} "
                    f"{(d.status or ''):<15} "
                    f"{d.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} DHCP configuration(s)")

    asyncio.run(run())


@cli.command("list-adsites")
@_shared_options
@click.option("--domain", default=None, help="Filter by AD domain name.")
def list_adsites_cmd(grid_url, username, password, wapi_ver, verify, domain):
    """List Active Directory sites discovered from Microsoft servers."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if domain:
                filters["domain"] = domain
            count = 0
            click.echo(f"{'Name':<35} {'UUID':<40} {'Ref'}")
            click.echo("-" * 110)
            async for site in client.microsoftserver.adsites_site.list(**filters):
                click.echo(
                    f"{(site.name or '')[:34]:<35} {(site.uuid or ''):<40} {site.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} AD site(s)")

    asyncio.run(run())


@cli.command("list-domains")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on domain name.")
def list_domains_cmd(grid_url, username, password, wapi_ver, verify, name_like):
    """List Active Directory domains discovered from Microsoft servers."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Name':<45} {'UUID':<40} {'Ref'}")
            click.echo("-" * 110)
            async for dom in client.microsoftserver.adsites_domain.list(**filters):
                click.echo(f"{(dom.name or '')[:44]:<45} {(dom.uuid or ''):<40} {dom.ref or ''}")
                count += 1
            click.echo(f"\nTotal: {count} AD domain(s)")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
