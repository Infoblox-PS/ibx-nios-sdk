# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Outbound Notifications - REST endpoints, templates, and rules (webhooks).

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL        - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME        - Admin username
    NIOS_PASSWORD        - Admin password
    NIOS_WAPI_VERSION    - Optional; default 2.14

Examples:
    # --- REST Endpoints ---
    python manage_notifications.py endpoints list
    python manage_notifications.py endpoints create --name "slack-hook" --uri "https://hooks.slack.com/..."
    python manage_notifications.py endpoints create --name "auth-hook" --uri "https://api.example.com/events" \\
        --wapi-username svc --wapi-password secret
    python manage_notifications.py endpoints delete "notification:rest:endpoint/ZG5z..."

    # --- Templates (system templates are read-only) ---
    python manage_notifications.py templates list
    python manage_notifications.py templates get "notification:rest:template/ZG5z..."

    # --- Rules ---
    python manage_notifications.py rules list
    python manage_notifications.py rules create \\
        --name "rpz-hit-alert" \\
        --endpoint "notification:rest:endpoint/ZG5z..." \\
        --template "notification:rest:template/ZG5z..." \\
        --event-type DNS_RPZ_HIT
    python manage_notifications.py rules delete "notification:rule/ZG5z..."
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
    """Manage NIOS outbound notification endpoints, templates, and rules."""


# ===========================================================================
# Endpoints sub-group
# ===========================================================================


@cli.group("endpoints")
def endpoints_group():
    """Manage REST notification endpoints (webhook receivers)."""


@endpoints_group.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on endpoint name.")
def endpoints_list(grid_url, username, password, wapi_ver, verify, name_like):
    """List REST notification endpoints."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Name':<30} {'URI':<50} {'Member Type':<13} {'Ref'}")
            click.echo("-" * 120)
            async for ep in client.notification.rest_endpoint.list(**filters):
                click.echo(
                    f"{(ep.name or '')[:29]:<30} "
                    f"{(ep.uri or '')[:49]:<50} "
                    f"{(ep.outbound_member_type or ''):<13} "
                    f"{ep.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} endpoint(s)")

    asyncio.run(run())


@endpoints_group.command("create")
@_shared_options
@click.option("--name", required=True, help="Endpoint name.")
@click.option("--uri", required=True, help="Webhook URI (e.g. https://hooks.slack.com/...).")
@click.option("--wapi-username", default=None, help="Username for authenticated endpoints.")
@click.option(
    "--wapi-password", default=None, hide_input=True, help="Password for authenticated endpoints."
)
@click.option(
    "--client-cert-token", default=None, help="Client certificate token (from fileop uploadinit)."
)
@click.option(
    "--outbound-member-type",
    type=click.Choice(["GM", "MEMBER"], case_sensitive=False),
    default="GM",
    show_default=True,
    help="Member type that sends outbound notifications (GM=Grid Master, MEMBER=specific member).",
)
@click.option("--comment", default=None, help="Optional comment.")
def endpoints_create(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    uri,
    wapi_username,
    wapi_password,
    client_cert_token,
    outbound_member_type,
    comment,
):
    """Create a REST notification endpoint."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "uri": uri,
                "outbound_member_type": outbound_member_type.upper(),
            }
            if wapi_username:
                payload["wapi_user_name"] = wapi_username
            if wapi_password:
                payload["wapi_user_password"] = wapi_password
            if client_cert_token:
                payload["client_certificate_token"] = client_cert_token
            if comment:
                payload["comment"] = comment
            ep = await client.notification.rest_endpoint.create(payload)
            click.echo(f"Created endpoint: {ep.name}")
            click.echo(f"  uri:                 {ep.uri}")
            click.echo(f"  outbound_member_type: {ep.outbound_member_type}")
            click.echo(f"  ref:                 {ep.ref}")

    asyncio.run(run())


@endpoints_group.command("delete")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this endpoint?")
def endpoints_delete(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a REST notification endpoint by ref.

    \b
    REF - WAPI object reference (e.g. notification:rest:endpoint/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.notification.rest_endpoint.delete(ref)
            click.echo(f"Deleted endpoint: {ref}")

    asyncio.run(run())


# ===========================================================================
# Templates sub-group
# ===========================================================================


@cli.group("templates")
def templates_group():
    """Browse REST notification templates (system templates are read-only)."""


@templates_group.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on template name.")
def templates_list(grid_url, username, password, wapi_ver, verify, name_like):
    """List notification REST templates."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Name':<40} {'Type':<12} {'Vendor':<20} {'Ref'}")
            click.echo("-" * 110)
            async for t in client.notification.rest_template.list(**filters):
                click.echo(
                    f"{(t.name or '')[:39]:<40} "
                    f"{(t.template_type or ''):<12} "
                    f"{(t.vendor_identifier or ''):<20} "
                    f"{t.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} template(s)")
            click.echo("\nNote: System-provided templates are read-only.")

    asyncio.run(run())


@templates_group.command("get")
@_shared_options
@click.argument("ref")
def templates_get(grid_url, username, password, wapi_ver, verify, ref):
    """Get a notification template by ref.

    \b
    REF - WAPI object reference (e.g. notification:rest:template/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            t = await client.notification.rest_template.get(ref)
            click.echo(f"Ref:               {t.ref}")
            click.echo(f"Name:              {t.name}")
            click.echo(f"Type:              {t.template_type}")
            click.echo(f"Vendor:            {t.vendor_identifier}")
            click.echo(f"Content Type:      {t.content_type}")
            if t.comment:
                click.echo(f"Comment:           {t.comment}")
            if t.template_parameters:
                click.echo("Parameters:")
                for p in t.template_parameters:
                    click.echo(f"  {p}")

    asyncio.run(run())


# ===========================================================================
# Rules sub-group
# ===========================================================================


@cli.group("rules")
def rules_group():
    """Manage notification rules (bind endpoints + templates to events)."""


@rules_group.command("list")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on rule name.")
@click.option(
    "--disable/--enable",
    "show_disabled",
    default=None,
    is_flag=True,
    help="Filter for disabled or enabled rules only.",
)
def rules_list(grid_url, username, password, wapi_ver, verify, name_like, show_disabled):
    """List notification rules."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Name':<35} {'Event Type':<25} {'Disabled':<10} {'Ref'}")
            click.echo("-" * 110)
            async for r in client.notification.rule.list(**filters):
                if show_disabled is not None and bool(r.disable) != show_disabled:
                    continue
                click.echo(
                    f"{(r.name or '')[:34]:<35} "
                    f"{(r.event_type or ''):<25} "
                    f"{str(r.disable or False):<10} "
                    f"{r.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} rule(s)")

    asyncio.run(run())


@rules_group.command("create")
@_shared_options
@click.option("--name", required=True, help="Rule name.")
@click.option(
    "--endpoint", required=True, help="REST endpoint WAPI ref (notification:rest:endpoint/...)."
)
@click.option(
    "--template", required=True, help="REST template WAPI ref (notification:rest:template/...)."
)
@click.option(
    "--event-type",
    default="DNS_RPZ_HIT",
    type=click.Choice(
        [
            "DNS_RPZ_HIT",
            "BFDDOWN",
            "DNS_QUERY_RATE_LIMIT",
            "DHCP_LEASE_NOTIFICATION",
            "DHCP_IPV4_LEASE_NOTIFICATION",
        ],
        case_sensitive=False,
    ),
    show_default=True,
    help="Event type that triggers the rule.",
)
@click.option("--comment", default=None, help="Optional comment.")
@click.option(
    "--all-members/--selected-members",
    default=True,
    show_default=True,
    help="Apply rule to all members or only selected members.",
)
@click.option("--disable/--enable", default=False, show_default=True, help="Disable the rule.")
def rules_create(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    endpoint,
    template,
    event_type,
    comment,
    all_members,
    disable,
):
    """Create a notification rule binding an endpoint and template to an event type."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "notification_action": endpoint,
                "notification_target": template,
                "event_type": event_type.upper(),
                "all_members": all_members,
                "disable": disable,
            }
            if comment:
                payload["comment"] = comment
            r = await client.notification.rule.create(payload)
            click.echo(f"Created rule: {r.name}")
            click.echo(f"  event_type: {r.event_type}")
            click.echo(f"  disabled:   {r.disable}")
            click.echo(f"  ref:        {r.ref}")

    asyncio.run(run())


@rules_group.command("delete")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this rule?")
def rules_delete(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a notification rule by ref.

    \b
    REF - WAPI object reference (e.g. notification:rule/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.notification.rule.delete(ref)
            click.echo(f"Deleted rule: {ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
