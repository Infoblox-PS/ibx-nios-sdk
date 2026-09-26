# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Threat Protection (ATP) and Threat Insight (TI).

Covers ATP profiles, rules, rulesets, rule templates, statistics, and TI
allowlists, module sets, and cloud client configuration.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL        - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME        - Admin username
    NIOS_PASSWORD        - Admin password
    NIOS_WAPI_VERSION    - Optional; default 2.14

Examples:
    # --- Threat Protection (ATP) ---
    python manage_threat_protection.py tp list-profiles
    python manage_threat_protection.py tp list-rules --profile "threatprotection:profile/ZG5z..."
    python manage_threat_protection.py tp list-rulesets
    python manage_threat_protection.py tp list-ruletemplates
    python manage_threat_protection.py tp create-profile --name "strict" --ruleset "threatprotection:ruleset/ZG5z..."
    python manage_threat_protection.py tp delete-profile "threatprotection:profile/ZG5z..."
    python manage_threat_protection.py tp stats

    # --- Threat Insight (TI) ---
    python manage_threat_protection.py ti list-allowlists
    python manage_threat_protection.py ti create-allowlist --fqdn "safe.example.com" --type CUSTOM
    python manage_threat_protection.py ti delete-allowlist "threatinsight:allowlist/ZG5z..."
    python manage_threat_protection.py ti list-modulesets
    python manage_threat_protection.py ti show-cloudclient
    python manage_threat_protection.py ti update-cloudclient --enable
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
    """Manage NIOS Threat Protection (ATP) profiles and Threat Insight (TI) configuration."""


# ===========================================================================
# tp sub-group - Threat Protection
# ===========================================================================


@cli.group("tp")
def tp_group():
    """Manage ATP profiles, rules, rulesets, and statistics."""


@tp_group.command("list-profiles")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on profile name.")
def tp_list_profiles(grid_url, username, password, wapi_ver, verify, name_like):
    """List Threat Protection profiles."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'Name':<35} {'Ruleset':<50} {'Ref'}")
            click.echo("-" * 120)
            async for p in client.threatprotection.profile.list(**filters):
                click.echo(
                    f"{(p.name or '')[:34]:<35} {(p.current_ruleset or '')[:49]:<50} {p.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} profile(s)")

    asyncio.run(run())


@tp_group.command("list-rules")
@_shared_options
@click.option(
    "--profile", "profile_ref", required=True, help="Threat Protection profile WAPI ref."
)
def tp_list_rules(grid_url, username, password, wapi_ver, verify, profile_ref):
    """List rules associated with a Threat Protection profile."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'SID':<12} {'Name':<40} {'Type':<12} {'Action':<12} {'Ref'}")
            click.echo("-" * 120)
            async for r in client.threatprotection.profile_rule.list(profile=profile_ref):
                click.echo(
                    f"{str(r.sid or ''):<12} "
                    f"{(r.name or '')[:39]:<40} "
                    f"{(r.type_ or r.model_extra.get('type') or ''):<12} "
                    f"{(r.action or ''):<12} "
                    f"{r.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} rule(s)")

    asyncio.run(run())


@tp_group.command("list-rulesets")
@_shared_options
def tp_list_rulesets(grid_url, username, password, wapi_ver, verify):
    """List available Threat Protection rulesets."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Version':<20} {'Type':<15} {'Active':<8} {'Ref'}")
            click.echo("-" * 100)
            async for rs in client.threatprotection.ruleset.list():
                click.echo(
                    f"{(rs.version or ''):<20} "
                    f"{(rs.type_ or rs.model_extra.get('type') or ''):<15} "
                    f"{str(rs.model_extra.get('is_default') or ''):<8} "
                    f"{rs.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} ruleset(s)")

    asyncio.run(run())


@tp_group.command("list-ruletemplates")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on rule template name.")
def tp_list_ruletemplates(grid_url, username, password, wapi_ver, verify, name_like):
    """List Threat Protection rule templates (read-only)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            count = 0
            click.echo(f"{'SID':<12} {'Name':<45} {'Category':<20} {'Ref'}")
            click.echo("-" * 110)
            async for t in client.threatprotection.ruletemplate.list(**filters):
                click.echo(
                    f"{str(t.sid or ''):<12} "
                    f"{(t.name or '')[:44]:<45} "
                    f"{(t.category or ''):<20} "
                    f"{t.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} rule template(s)")

    asyncio.run(run())


@tp_group.command("create-profile")
@_shared_options
@click.option("--name", required=True, help="Profile name.")
@click.option("--ruleset", required=True, help="Ruleset WAPI ref (threatprotection:ruleset/...).")
@click.option("--comment", default=None, help="Optional comment.")
def tp_create_profile(grid_url, username, password, wapi_ver, verify, name, ruleset, comment):
    """Create a new Threat Protection profile bound to a ruleset."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "current_ruleset": ruleset}
            if comment:
                payload["comment"] = comment
            p = await client.threatprotection.profile.create(payload)
            click.echo(f"Created TP profile: {p.name}")
            click.echo(f"  ruleset: {p.current_ruleset}")
            click.echo(f"  ref:     {p.ref}")

    asyncio.run(run())


@tp_group.command("delete-profile")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this TP profile?")
def tp_delete_profile(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a Threat Protection profile by ref.

    \b
    REF - WAPI object reference (e.g. threatprotection:profile/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.threatprotection.profile.delete(ref)
            click.echo(f"Deleted TP profile: {ref}")

    asyncio.run(run())


@tp_group.command("stats")
@_shared_options
@click.option("--member", default=None, help="Filter statistics by grid member.")
def tp_stats(grid_url, username, password, wapi_ver, verify, member):
    """Display Threat Protection statistics (read-only)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if member:
                filters["member"] = member
            count = 0
            click.echo(f"{'Member':<30} {'Ref'}")
            click.echo("-" * 80)
            async for s in client.threatprotection.statistics.list(**filters):
                click.echo(f"{(s.member or '')[:29]:<30} {s.ref or ''}")
                # Print any counters available
                for k, v in (s.model_extra or {}).items():
                    if k not in ("_ref",):
                        click.echo(f"  {k}: {v}")
                count += 1
            click.echo(f"\nTotal: {count} statistics record(s)")

    asyncio.run(run())


# ===========================================================================
# ti sub-group - Threat Insight
# ===========================================================================


@cli.group("ti")
def ti_group():
    """Manage Threat Insight allowlists, module sets, and cloud client configuration."""


@ti_group.command("list-allowlists")
@_shared_options
@click.option("--fqdn-like", default=None, help="Substring filter on FQDN.")
@click.option(
    "--type",
    "list_type",
    type=click.Choice(["SYSTEM", "CUSTOM"], case_sensitive=False),
    default=None,
    help="Filter by allowlist type.",
)
def ti_list_allowlists(grid_url, username, password, wapi_ver, verify, fqdn_like, list_type):
    """List Threat Insight allowlist entries."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if fqdn_like:
                filters["fqdn__like"] = fqdn_like
            if list_type:
                filters["type"] = list_type.upper()
            count = 0
            click.echo(f"{'FQDN':<45} {'Type':<10} {'Disabled':<10} {'Comment'}")
            click.echo("-" * 100)
            async for al in client.threatinsight.allowlist.list(**filters):
                click.echo(
                    f"{(al.fqdn or '')[:44]:<45} "
                    f"{(al.type_ or ''):<10} "
                    f"{str(al.disable or False):<10} "
                    f"{al.comment or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} allowlist entry/entries")

    asyncio.run(run())


@ti_group.command("create-allowlist")
@_shared_options
@click.option("--fqdn", required=True, help="Fully-qualified domain name to allowlist.")
@click.option(
    "--type",
    "list_type",
    type=click.Choice(["CUSTOM"], case_sensitive=False),
    default="CUSTOM",
    show_default=True,
    help="Allowlist type (only CUSTOM can be created via API).",
)
@click.option("--comment", default=None, help="Optional comment.")
@click.option(
    "--disable/--enable", default=False, show_default=True, help="Disable the allowlist entry."
)
def ti_create_allowlist(
    grid_url, username, password, wapi_ver, verify, fqdn, list_type, comment, disable
):
    """Create a Threat Insight allowlist entry for a domain."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"fqdn": fqdn, "disable": disable}
            if comment:
                payload["comment"] = comment
            al = await client.threatinsight.allowlist.create(payload)
            click.echo(f"Created TI allowlist entry: {al.fqdn}")
            click.echo(f"  type:    {al.type_}")
            click.echo(f"  ref:     {al.ref}")

    asyncio.run(run())


@ti_group.command("delete-allowlist")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this TI allowlist entry?")
def ti_delete_allowlist(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a Threat Insight allowlist entry by ref.

    \b
    REF - WAPI object reference (e.g. threatinsight:allowlist/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.threatinsight.allowlist.delete(ref)
            click.echo(f"Deleted TI allowlist entry: {ref}")

    asyncio.run(run())


@ti_group.command("list-modulesets")
@_shared_options
def ti_list_modulesets(grid_url, username, password, wapi_ver, verify):
    """List Threat Insight module sets (read-only, Infoblox-managed)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Ref':<60} {'Details'}")
            click.echo("-" * 100)
            async for ms in client.threatinsight.moduleset.list():
                details = str(ms.model_extra) if ms.model_extra else ""
                click.echo(f"{(ms.ref or ''):<60} {details[:60]}")
                count += 1
            click.echo(f"\nTotal: {count} module set(s)")
            click.echo("\nNote: Module sets are managed by Infoblox and are read-only.")

    asyncio.run(run())


@ti_group.command("show-cloudclient")
@_shared_options
def ti_show_cloudclient(grid_url, username, password, wapi_ver, verify):
    """Show the Threat Insight cloud client configuration (singleton)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # The cloudclient is a singleton - list returns at most one entry
            cc = await client.threatinsight.cloudclient.find_one()
            if cc is None:
                click.echo("No Threat Insight cloud client configuration found.")
                return
            click.echo(f"Ref:                {cc.ref}")
            click.echo(f"Enabled:            {cc.enable}")
            if cc.blacklist_rpz_list:
                click.echo("Blacklist RPZ list:")
                for rpz in cc.blacklist_rpz_list:
                    click.echo(f"  {rpz}")
            for k, v in (cc.model_extra or {}).items():
                if k not in ("_ref",):
                    click.echo(f"{k}: {v}")

    asyncio.run(run())


@ti_group.command("update-cloudclient")
@_shared_options
@click.option(
    "--enable/--disable", required=True, help="Enable or disable the Threat Insight cloud client."
)
@click.option(
    "--force-refresh",
    is_flag=True,
    default=False,
    help="Force a refresh of cloud intelligence data.",
)
def ti_update_cloudclient(grid_url, username, password, wapi_ver, verify, enable, force_refresh):
    """Enable or disable the Threat Insight cloud client (singleton)."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            cc = await client.threatinsight.cloudclient.find_one()
            if cc is None:
                raise click.ClickException("Threat Insight cloud client configuration not found.")
            payload = {"enable": enable}
            if force_refresh:
                payload["force_refresh"] = True
            updated = await client.threatinsight.cloudclient.update(cc.ref, payload)
            status = "enabled" if updated.enable else "disabled"
            click.echo(f"Threat Insight cloud client {status}.")
            click.echo(f"  ref: {updated.ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
