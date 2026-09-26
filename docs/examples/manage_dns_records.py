# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS DNS records - A, AAAA, CNAME, MX, TXT, and HOST records.

Create, list, and delete common DNS record types using the ibx-nios-sdk WAPI
client. A single `delete` subcommand accepts the WAPI ref of any record type.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL     - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME     - Admin username
    NIOS_PASSWORD     - Admin password
    NIOS_WAPI_VERSION - Optional; default 2.14

Examples:
    # List A records in a zone
    python manage_dns_records.py list-a --zone example.com --view default

    # Create an A record
    python manage_dns_records.py create-a --name host.example.com --ipv4addr 10.0.0.1

    # Create a CNAME
    python manage_dns_records.py create-cname --name alias.example.com --canonical host.example.com

    # Create an MX record
    python manage_dns_records.py create-mx --name example.com --mail-exchanger mail.example.com --preference 10

    # Create a HOST record (multiple IPs)
    python manage_dns_records.py create-host --name host.example.com --ipv4addrs 10.0.0.1 --ipv4addrs 10.0.0.2

    # Delete any record type by ref
    python manage_dns_records.py delete record:a/ZG5z...
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
    """Manage NIOS DNS records (A, AAAA, CNAME, MX, TXT, HOST)."""


@cli.command("list-a")
@_shared_options
@click.option("--zone", default=None, help="Filter by zone FQDN.")
@click.option("--view", default=None, help="Filter by DNS view name.")
@click.option("--name-like", default=None, help="Substring filter on record name.")
@click.option(
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit results as a JSON array on stdout (for scripting).",
)
def list_a_cmd(grid_url, username, password, wapi_ver, verify, zone, view, name_like, json_output):
    """List DNS A records."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if zone:
                filters["zone"] = zone
            if view:
                filters["view"] = view
            if name_like:
                filters["name__like"] = name_like
            if json_output:
                rows = [r async for r in client.dns.record_a.list(**filters)]
                _dump_json(rows)
                return
            count = 0
            click.echo(f"{'Name':<40} {'IPv4':<16} {'View':<12} {'Zone':<30} {'Comment'}")
            click.echo("-" * 110)
            async for r in client.dns.record_a.list(**filters):
                click.echo(
                    f"{(r.name or '')[:39]:<40} "
                    f"{(r.ipv4addr or ''):<16} "
                    f"{(r.view or ''):<12} "
                    f"{(r.zone or '')[:29]:<30} "
                    f"{r.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("create-a")
@_shared_options
@click.option("--name", required=True, help="Fully-qualified hostname (e.g. host.example.com).")
@click.option("--ipv4addr", required=True, help="IPv4 address.")
@click.option("--view", default=None, help="DNS view (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
@click.option("--ttl", default=None, type=int, help="Optional TTL override in seconds.")
def create_a_cmd(
    grid_url, username, password, wapi_ver, verify, name, ipv4addr, view, comment, ttl
):
    """Create a DNS A record."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "ipv4addr": ipv4addr}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            if ttl is not None:
                payload["ttl"] = ttl
                payload["use_ttl"] = True
            r = await client.dns.record_a.create(payload)
            click.echo(f"Created A record: {r.name} -> {r.ipv4addr}")
            click.echo(f"  ref: {r.ref}")

    asyncio.run(run())


@cli.command("create-aaaa")
@_shared_options
@click.option("--name", required=True, help="Fully-qualified hostname.")
@click.option("--ipv6addr", required=True, help="IPv6 address.")
@click.option("--view", default=None, help="DNS view (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_aaaa_cmd(grid_url, username, password, wapi_ver, verify, name, ipv6addr, view, comment):
    """Create a DNS AAAA record."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "ipv6addr": ipv6addr}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            r = await client.dns.record_aaaa.create(payload)
            click.echo(f"Created AAAA record: {r.name} -> {r.ipv6addr}")
            click.echo(f"  ref: {r.ref}")

    asyncio.run(run())


@cli.command("create-cname")
@_shared_options
@click.option("--name", required=True, help="Alias hostname (e.g. alias.example.com).")
@click.option("--canonical", required=True, help="Canonical (target) hostname.")
@click.option("--view", default=None, help="DNS view (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_cname_cmd(
    grid_url, username, password, wapi_ver, verify, name, canonical, view, comment
):
    """Create a DNS CNAME record."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "canonical": canonical}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            r = await client.dns.record_cname.create(payload)
            click.echo(f"Created CNAME record: {r.name} -> {r.canonical}")
            click.echo(f"  ref: {r.ref}")

    asyncio.run(run())


@cli.command("create-mx")
@_shared_options
@click.option("--name", required=True, help="Owner name (usually zone FQDN).")
@click.option("--mail-exchanger", required=True, help="Mail exchanger hostname.")
@click.option("--preference", required=True, type=int, help="MX preference (priority) value.")
@click.option("--view", default=None, help="DNS view (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_mx_cmd(
    grid_url, username, password, wapi_ver, verify, name, mail_exchanger, preference, view, comment
):
    """Create a DNS MX record."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "mail_exchanger": mail_exchanger, "preference": preference}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            r = await client.dns.record_mx.create(payload)
            click.echo(f"Created MX record: {r.name} -> {r.mail_exchanger} (pref {r.preference})")
            click.echo(f"  ref: {r.ref}")

    asyncio.run(run())


@cli.command("create-txt")
@_shared_options
@click.option("--name", required=True, help="Owner name.")
@click.option("--text", required=True, help="TXT record content string.")
@click.option("--view", default=None, help="DNS view (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_txt_cmd(grid_url, username, password, wapi_ver, verify, name, text, view, comment):
    """Create a DNS TXT record."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "text": text}
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            r = await client.dns.record_txt.create(payload)
            click.echo(f"Created TXT record: {r.name}")
            click.echo(f"  ref:  {r.ref}")
            click.echo(f"  text: {r.text}")

    asyncio.run(run())


@cli.command("create-host")
@_shared_options
@click.option("--name", required=True, help="Fully-qualified hostname.")
@click.option(
    "--ipv4addrs",
    multiple=True,
    required=True,
    help="IPv4 address(es) - repeat for multiple: --ipv4addrs 10.0.0.1 --ipv4addrs 10.0.0.2",
)
@click.option("--view", default=None, help="DNS view (omit for grid default).")
@click.option("--comment", default=None, help="Optional comment.")
def create_host_cmd(
    grid_url, username, password, wapi_ver, verify, name, ipv4addrs, view, comment
):
    """Create a DNS HOST record (combines A + PTR records)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "ipv4addrs": [{"ipv4addr": ip} for ip in ipv4addrs],
            }
            if view:
                payload["view"] = view
            if comment:
                payload["comment"] = comment
            r = await client.dns.record_host.create(payload)
            click.echo(f"Created HOST record: {r.name}")
            click.echo(f"  ref: {r.ref}")
            if r.ipv4addrs:
                for addr in r.ipv4addrs:
                    ip = addr.ipv4addr if hasattr(addr, "ipv4addr") else str(addr)
                    click.echo(f"  ip:  {ip}")

    asyncio.run(run())


@cli.command("delete")
@_shared_options
@click.argument("ref")
def delete_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a DNS record of any type by its WAPI reference.

    \b
    REF - WAPI object reference (e.g. record:a/ZG5z..., record:cname/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # Route to the correct resource based on the ref prefix
            rtype = ref.split("/")[0]
            resource_map = {
                "record:a": client.dns.record_a,
                "record:aaaa": client.dns.record_aaaa,
                "record:cname": client.dns.record_cname,
                "record:mx": client.dns.record_mx,
                "record:txt": client.dns.record_txt,
                "record:host": client.dns.record_host,
                "record:ptr": client.dns.record_ptr,
                "record:srv": client.dns.record_srv,
            }
            resource = resource_map.get(rtype)
            if resource is None:
                raise click.ClickException(
                    f"Unrecognized record type '{rtype}'. Supported: {list(resource_map)}"
                )
            await resource.delete(ref)
            click.echo(f"Deleted {rtype} record: {ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
