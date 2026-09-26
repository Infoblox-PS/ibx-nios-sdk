# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS authentication services - LDAP, RADIUS, TACACS+, AD, SAML, and CA certs.

List, create, and delete authentication service objects across all supported
types, and inspect CA certificate details via the ibx-nios-sdk WAPI client.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables:
    NIOS_GRID_URL      - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME      - Admin username
    NIOS_PASSWORD      - Admin password
    NIOS_WAPI_VERSION  - Optional; default 2.14

Examples:
    # List all authentication services (combined view)
    python manage_auth_services.py list-services

    # Add an LDAP auth service
    python manage_auth_services.py add-ldap --name corp-ldap --ldap-server ldap.example.com \\
        --search-base "dc=example,dc=com" --bind-dn "cn=reader,dc=example,dc=com"

    # Add a RADIUS auth service
    python manage_auth_services.py add-radius --name corp-radius --server 10.0.0.5 \\
        --shared-secret topsecret

    # Delete an auth service by WAPI ref (any type)
    python manage_auth_services.py delete-service ldap_auth_service/ZG5z...:corp-ldap

    # List CA certificates
    python manage_auth_services.py list-ca-certs

    # Show a specific CA certificate
    python manage_auth_services.py show-cert cacertificate/ZG5z...:sha256fingerprint
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
    """Manage NIOS authentication services and CA certificates."""


@cli.command("list-services")
@_shared_options
def list_services(grid_url, username, password, wapi_ver, verify):
    """List every auth service type in a combined view."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            total = 0
            click.echo(f"{'Type':<22} {'Name':<30} {'Comment'}")
            click.echo("-" * 80)

            async for svc in client.security.ad_auth_service.list():
                click.echo(f"{'AD':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            async for svc in client.security.ldap_auth_service.list():
                click.echo(f"{'LDAP':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            async for svc in client.security.radius_authservice.list():
                click.echo(f"{'RADIUS':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            async for svc in client.security.tacacsplus_authservice.list():
                click.echo(f"{'TACACS+':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            async for svc in client.security.saml_authservice.list():
                click.echo(f"{'SAML':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            async for svc in client.security.localuser_authservice.list():
                click.echo(f"{'Local User':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            async for svc in client.security.certificate_authservice.list():
                click.echo(f"{'Certificate':<22} {(svc.name or ''):<30} {svc.comment or ''}")
                total += 1

            click.echo(f"\nTotal: {total}")

    asyncio.run(run())


@cli.command("add-ldap")
@_shared_options
@click.option("--name", required=True, help="Unique name for this LDAP service.")
@click.option(
    "--ldap-server",
    required=True,
    metavar="HOST",
    help="Hostname or IP address of the LDAP server.",
)
@click.option(
    "--search-base",
    required=True,
    metavar="DN",
    help="Base DN for user searches (e.g. dc=example,dc=com).",
)
@click.option(
    "--bind-dn", required=True, metavar="DN", help="DN used to bind to the LDAP directory."
)
@click.option(
    "--bind-password",
    default=None,
    hide_input=True,
    help="Password for the bind DN (prompted if not set).",
)
@click.option("--port", default=389, show_default=True, type=int, help="LDAP server port.")
@click.option("--use-ssl/--no-ssl", default=False, show_default=True, help="Use LDAPS (TLS).")
@click.option("--comment", default=None, help="Optional comment.")
def add_ldap(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    ldap_server,
    search_base,
    bind_dn,
    bind_password,
    port,
    use_ssl,
    comment,
):
    """Add an LDAP authentication service."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            server_entry: dict = {
                "address": ldap_server,
                "port": port,
                "use_ssl": use_ssl,
            }
            payload: dict = {
                "name": name,
                "ldap_user_attribute": "sAMAccountName",
                "search_scope": "SUB",
                "base_dn": search_base,
                "bind_user_dn": bind_dn,
                "servers": [server_entry],
            }
            if bind_password:
                payload["bind_password"] = bind_password
            if comment:
                payload["comment"] = comment
            svc = await client.security.ldap_auth_service.create(payload)
            click.echo(f"Created LDAP auth service: {svc.name}")
            click.echo(f"  ref: {svc.ref}")

    asyncio.run(run())


@cli.command("add-radius")
@_shared_options
@click.option("--name", required=True, help="Unique name for this RADIUS service.")
@click.option(
    "--server", required=True, metavar="HOST", help="Hostname or IP address of the RADIUS server."
)
@click.option(
    "--auth-port", default=1812, show_default=True, type=int, help="RADIUS authentication port."
)
@click.option(
    "--shared-secret", default=None, hide_input=True, help="Shared secret for the RADIUS server."
)
@click.option(
    "--acct-port", default=1813, show_default=True, type=int, help="RADIUS accounting port."
)
@click.option("--comment", default=None, help="Optional comment.")
def add_radius(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    server,
    auth_port,
    shared_secret,
    acct_port,
    comment,
):
    """Add a RADIUS authentication service."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            server_entry: dict = {
                "address": server,
                "auth_port": auth_port,
                "acct_port": acct_port,
            }
            if shared_secret:
                server_entry["shared_secret"] = shared_secret
            payload: dict = {
                "name": name,
                "servers": [server_entry],
            }
            if comment:
                payload["comment"] = comment
            svc = await client.security.radius_authservice.create(payload)
            click.echo(f"Created RADIUS auth service: {svc.name}")
            click.echo(f"  ref: {svc.ref}")

    asyncio.run(run())


@cli.command("delete-service")
@_shared_options
@click.argument("ref")
def delete_service(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an authentication service by WAPI reference (any type).

    \b
    REF - WAPI object reference, e.g.:
          ldap_auth_service/ZG5z...:corp-ldap
          radius:authservice/ZG5z...:corp-radius
          tacacsplus:authservice/ZG5z...:corp-tacacs
          ad_auth_service/ZG5z...:corp-ad
          saml:authservice/ZG5z...:corp-saml
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            ref_lower = ref.lower()
            if ref_lower.startswith("ad_auth_service/"):
                await client.security.ad_auth_service.delete(ref)
            elif ref_lower.startswith("ldap_auth_service/"):
                await client.security.ldap_auth_service.delete(ref)
            elif ref_lower.startswith("radius:authservice/"):
                await client.security.radius_authservice.delete(ref)
            elif ref_lower.startswith("tacacsplus:authservice/"):
                await client.security.tacacsplus_authservice.delete(ref)
            elif ref_lower.startswith("saml:authservice/"):
                await client.security.saml_authservice.delete(ref)
            elif ref_lower.startswith("localuser:authservice/"):
                raise click.ClickException(
                    "WAPI does not support deleting localuser:authservice - the local "
                    "user database service is built in and read-only. Disable it from "
                    "the authentication policy instead."
                )
            elif ref_lower.startswith("certificate:authservice/"):
                await client.security.certificate_authservice.delete(ref)
            else:
                raise click.ClickException(
                    f"Unrecognised auth service ref prefix: {ref!r}\n"
                    "Supported prefixes: ad_auth_service, ldap_auth_service, "
                    "radius:authservice, tacacsplus:authservice, saml:authservice, "
                    "certificate:authservice"
                )
            click.echo(f"Deleted auth service: {ref}")

    asyncio.run(run())


@cli.command("list-ca-certs")
@_shared_options
def list_ca_certs(grid_url, username, password, wapi_ver, verify):
    """List CA certificates installed on the Grid."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Distinguished Name':<50} {'Issuer':<40} {'Serial'}")
            click.echo("-" * 110)
            async for cert in client.security.cacertificate.list():
                click.echo(
                    f"{(cert.distinguished_name or '')[:49]:<50} "
                    f"{(cert.issuer or '')[:39]:<40} "
                    f"{cert.serial or ''}"
                )
                count += 1
            if count == 0:
                click.echo("No CA certificates found.")
            else:
                click.echo(f"\nTotal: {count}")

    asyncio.run(run())


@cli.command("show-cert")
@_shared_options
@click.argument("ref")
def show_cert(grid_url, username, password, wapi_ver, verify, ref):
    """Show full details of a CA certificate by WAPI reference.

    \b
    REF - WAPI object reference (e.g. cacertificate/ZG5z...:fingerprint)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            cert = await client.security.cacertificate.get(ref)
            click.echo(f"  ref:                {cert.ref}")
            click.echo(f"  distinguished_name: {cert.distinguished_name or 'N/A'}")
            click.echo(f"  issuer:             {cert.issuer or 'N/A'}")
            click.echo(f"  serial:             {cert.serial or 'N/A'}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
