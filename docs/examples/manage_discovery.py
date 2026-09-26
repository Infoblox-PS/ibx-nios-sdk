# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Network Discovery - devices, credential groups, diagnostic tasks, vDiscovery.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL        - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME        - Admin username
    NIOS_PASSWORD        - Admin password
    NIOS_WAPI_VERSION    - Optional; default 2.14

Examples:
    # List all discovered devices
    python manage_discovery.py list-devices

    # Filter devices by name substring and type
    python manage_discovery.py list-devices --name-like "switch" --type SWITCH

    # Get a specific device by ref
    python manage_discovery.py get-device "discovery:device/ZG5z..."

    # List device components for a device
    python manage_discovery.py list-device-components --device-ref "discovery:device/ZG5z..."

    # List device interfaces
    python manage_discovery.py list-device-interfaces --device-ref "discovery:device/ZG5z..."

    # List credential groups
    python manage_discovery.py list-credential-groups

    # Create a credential group
    python manage_discovery.py create-credential-group --name "Core-Switches"

    # List diagnostic tasks
    python manage_discovery.py list-diagnostic-tasks

    # Show one diagnostic task
    python manage_discovery.py show-diagnostic-task "discovery:diagnostictask/ZG5z..."

    # List vDiscovery tasks
    python manage_discovery.py list-vdiscovery-tasks

    # Create a vDiscovery task
    python manage_discovery.py create-vdiscovery-task --name "aws-prod" --driver-type AWS --account-id "123456789012"
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
    """Manage NIOS Network Discovery - devices, credentials, diagnostics, vDiscovery."""


# ---------------------------------------------------------------------------
# Devices
# ---------------------------------------------------------------------------


@cli.command("list-devices")
@_shared_options
@click.option("--name-like", default=None, help="Substring filter on device name.")
@click.option(
    "--type", "device_type", default=None, help="Filter by device type (e.g. SWITCH, ROUTER)."
)
def list_devices_cmd(grid_url, username, password, wapi_ver, verify, name_like, device_type):
    """List discovered network devices."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if name_like:
                filters["name__like"] = name_like
            if device_type:
                filters["type"] = device_type
            count = 0
            click.echo(f"{'Name':<35} {'Address':<18} {'Type':<15} {'Ref'}")
            click.echo("-" * 100)
            async for d in client.discovery.device.list(**filters):
                click.echo(
                    f"{(d.name or '')[:34]:<35} "
                    f"{(d.address or ''):<18} "
                    f"{(d.type_ or d.model_extra.get('type') or ''):<15} "
                    f"{d.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} device(s)")

    asyncio.run(run())


@cli.command("get-device")
@_shared_options
@click.argument("ref")
def get_device_cmd(grid_url, username, password, wapi_ver, verify, ref):
    """Get a specific discovered device by its WAPI reference.

    \b
    REF - WAPI object reference (e.g. discovery:device/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            d = await client.discovery.device.get(ref)
            click.echo(f"Ref:     {d.ref}")
            click.echo(f"Name:    {d.name}")
            click.echo(f"Address: {d.address}")

    asyncio.run(run())


@cli.command("list-device-components")
@_shared_options
@click.option("--device-ref", default=None, help="Filter by device WAPI reference.")
@click.option("--device-name", default=None, help="Filter by device name (exact).")
def list_device_components_cmd(
    grid_url, username, password, wapi_ver, verify, device_ref, device_name
):
    """List components for a discovered device."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if device_ref:
                filters["device"] = device_ref
            if device_name:
                filters["device_name"] = device_name
            count = 0
            click.echo(f"{'Ref':<50} {'Type':<20} {'Name'}")
            click.echo("-" * 100)
            async for c in client.discovery.devicecomponent.list(**filters):
                click.echo(
                    f"{(c.ref or '')[:49]:<50} "
                    f"{(c.model_extra.get('component_type') or ''):<20} "
                    f"{c.model_extra.get('name') or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} component(s)")

    asyncio.run(run())


@cli.command("list-device-interfaces")
@_shared_options
@click.option("--device-ref", required=True, help="Filter by device WAPI reference.")
def list_device_interfaces_cmd(grid_url, username, password, wapi_ver, verify, device_ref):
    """List interfaces for a discovered device."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Ref':<50} {'Name':<25} {'IP Address'}")
            click.echo("-" * 100)
            async for iface in client.discovery.deviceinterface.list(device=device_ref):
                click.echo(
                    f"{(iface.ref or '')[:49]:<50} "
                    f"{(iface.model_extra.get('name') or ''):<25} "
                    f"{iface.model_extra.get('ip_address') or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} interface(s)")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Credential Groups
# ---------------------------------------------------------------------------


@cli.command("list-credential-groups")
@_shared_options
def list_credential_groups_cmd(grid_url, username, password, wapi_ver, verify):
    """List discovery credential groups."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<35} {'UUID':<40} {'Ref'}")
            click.echo("-" * 110)
            async for g in client.discovery.credentialgroup.list():
                click.echo(f"{(g.name or '')[:34]:<35} {(g.uuid or ''):<40} {g.ref or ''}")
                count += 1
            click.echo(f"\nTotal: {count} credential group(s)")

    asyncio.run(run())


@cli.command("create-credential-group")
@_shared_options
@click.option("--name", required=True, help="Name for the new credential group.")
@click.option("--comment", default=None, help="Optional comment.")
def create_credential_group_cmd(grid_url, username, password, wapi_ver, verify, name, comment):
    """Create a new discovery credential group."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name}
            if comment:
                payload["comment"] = comment
            g = await client.discovery.credentialgroup.create(payload)
            click.echo(f"Created credential group: {g.name}")
            click.echo(f"  ref: {g.ref}")
            if g.uuid:
                click.echo(f"  uuid: {g.uuid}")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Diagnostic Tasks
# ---------------------------------------------------------------------------


@cli.command("list-diagnostic-tasks")
@_shared_options
@click.option("--ip-address", default=None, help="Filter by target IP address.")
def list_diagnostic_tasks_cmd(grid_url, username, password, wapi_ver, verify, ip_address):
    """List discovery diagnostic tasks."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if ip_address:
                filters["ip_address"] = ip_address
            count = 0
            click.echo(f"{'Task ID':<40} {'IP Address':<18} {'Network View':<20} {'Ref'}")
            click.echo("-" * 110)
            async for t in client.discovery.diagnostictask.list(**filters):
                click.echo(
                    f"{(t.task_id or ''):<40} "
                    f"{(t.ip_address or ''):<18} "
                    f"{(t.network_view or ''):<20} "
                    f"{t.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} diagnostic task(s)")

    asyncio.run(run())


@cli.command("show-diagnostic-task")
@_shared_options
@click.argument("task_ref")
def show_diagnostic_task_cmd(grid_url, username, password, wapi_ver, verify, task_ref):
    """Show one discovery diagnostic task.

    \b
    TASK_REF - WAPI ref of the diagnostic task (e.g. discovery:diagnostictask/ZG5z...)

    WAPI restricts create, update and delete on discovery:diagnostictask, so this
    object can only be read. Diagnostics are started from the NIOS UI (Data
    Management -> Devices -> Diagnostics); the SDK raises
    UnsupportedOperationError if you try to write to it.
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            t = await client.discovery.diagnostictask.get(task_ref)
            click.echo(f"Diagnostic task: {t.ref}")
            click.echo(f"  task_id:      {t.task_id}")
            click.echo(f"  ip_address:   {t.ip_address}")
            click.echo(f"  network_view: {t.network_view}")
            click.echo(f"  start_time:   {t.start_time}")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# vDiscovery Tasks
# ---------------------------------------------------------------------------


@cli.command("list-vdiscovery-tasks")
@_shared_options
@click.option("--driver-type", default=None, help="Filter by driver type (e.g. AWS, AZURE, GCP).")
def list_vdiscovery_tasks_cmd(grid_url, username, password, wapi_ver, verify, driver_type):
    """List vDiscovery (virtual/cloud) tasks."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if driver_type:
                filters["driver_type"] = driver_type
            count = 0
            click.echo(f"{'Name':<30} {'Driver':<10} {'State':<15} {'Enabled':<8} {'Ref'}")
            click.echo("-" * 110)
            async for t in client.discovery.vdiscoverytask.list(**filters):
                click.echo(
                    f"{(t.name or '')[:29]:<30} "
                    f"{(t.driver_type or ''):<10} "
                    f"{(t.state or ''):<15} "
                    f"{str(t.enabled or ''):<8} "
                    f"{t.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} vDiscovery task(s)")

    asyncio.run(run())


@cli.command("create-vdiscovery-task")
@_shared_options
@click.option("--name", required=True, help="Name for the vDiscovery task.")
@click.option(
    "--driver-type",
    required=True,
    type=click.Choice(["AWS", "AZURE", "GCP", "OPENSTACK"], case_sensitive=False),
    help="Cloud platform driver type.",
)
@click.option("--account-id", default=None, help="Cloud account/subscription/project ID.")
@click.option("--member", default=None, help="Grid member to run the task on.")
@click.option("--comment", default=None, help="Optional comment.")
@click.option("--enable/--disable", default=True, show_default=True, help="Enable the task.")
def create_vdiscovery_task_cmd(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    driver_type,
    account_id,
    member,
    comment,
    enable,
):
    """Create a new vDiscovery (virtual/cloud) task."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "driver_type": driver_type.upper(),
                "enabled": enable,
            }
            if account_id:
                payload["accounts_list"] = account_id
            if member:
                payload["member"] = member
            if comment:
                payload["comment"] = comment
            t = await client.discovery.vdiscoverytask.create(payload)
            click.echo(f"Created vDiscovery task: {t.name}")
            click.echo(f"  driver_type: {t.driver_type}")
            click.echo(f"  enabled:     {t.enabled}")
            click.echo(f"  ref:         {t.ref}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
