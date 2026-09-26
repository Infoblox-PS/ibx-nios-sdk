# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS Cloud DNS - AWS Route53, Azure DNS, GCP DNS task groups, users, and multi-regions.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL        - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME        - Admin username
    NIOS_PASSWORD        - Admin password
    NIOS_WAPI_VERSION    - Optional; default 2.14

Examples:
    # --- AWS ---
    python manage_cloud.py aws list-task-groups
    python manage_cloud.py aws create-task-group --name "prod-aws" --account-id "123456789012"
    python manage_cloud.py aws delete-task-group "awsrte53taskgroup/ZG5z..."
    python manage_cloud.py aws list-users
    python manage_cloud.py aws create-user --name "svc-aws" --access-key AKIA... --secret-key "..."

    # --- Azure ---
    python manage_cloud.py azure list-task-groups
    python manage_cloud.py azure create-task-group --name "prod-azure" --subscription-id "xxxxxxxx-..."
    python manage_cloud.py azure delete-task-group "azurednstaskgroup/ZG5z..."
    python manage_cloud.py azure list-users
    python manage_cloud.py azure create-user --name "svc-azure" --tenant-id "xxxx" --client-id "xxxx"

    # --- GCP ---
    python manage_cloud.py gcp list-task-groups
    python manage_cloud.py gcp create-task-group --name "prod-gcp" --project-id "my-project"
    python manage_cloud.py gcp delete-task-group "gcpdnstaskgroup/ZG5z..."
    python manage_cloud.py gcp list-users
    python manage_cloud.py gcp create-user --name "svc-gcp" --account-email "svc@project.iam.gserviceaccount.com"

    # --- Multi-regions ---
    python manage_cloud.py list-multiregions
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
    """Manage NIOS Cloud DNS integrations - AWS, Azure, GCP, and multi-regions."""


# ===========================================================================
# AWS sub-group
# ===========================================================================


@cli.group("aws")
def aws_group():
    """Manage AWS Route53 task groups and users."""


@aws_group.command("list-task-groups")
@_shared_options
@click.option("--account-id", default=None, help="Filter by AWS Account ID.")
def aws_list_task_groups(grid_url, username, password, wapi_ver, verify, account_id):
    """List AWS Route53 task groups."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if account_id:
                filters["account_id"] = account_id
            count = 0
            click.echo(f"{'Name':<30} {'Account ID':<20} {'Status':<15} {'Ref'}")
            click.echo("-" * 100)
            async for g in client.cloud.awsrte53taskgroup.list(**filters):
                click.echo(
                    f"{(g.name or '')[:29]:<30} "
                    f"{(g.account_id or ''):<20} "
                    f"{(g.sync_status or ''):<15} "
                    f"{g.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} AWS task group(s)")

    asyncio.run(run())


@aws_group.command("create-task-group")
@_shared_options
@click.option("--name", required=True, help="Task group name.")
@click.option("--account-id", required=True, help="AWS Account ID.")
@click.option("--grid-member", default=None, help="Grid member to run tasks on.")
@click.option("--comment", default=None, help="Optional comment.")
@click.option("--disable/--enable", default=False, show_default=True, help="Disable task group.")
def aws_create_task_group(
    grid_url, username, password, wapi_ver, verify, name, account_id, grid_member, comment, disable
):
    """Create an AWS Route53 task group."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "account_id": account_id, "disabled": disable}
            if grid_member:
                payload["grid_member"] = grid_member
            if comment:
                payload["comment"] = comment
            g = await client.cloud.awsrte53taskgroup.create(payload)
            click.echo(f"Created AWS task group: {g.name}")
            click.echo(f"  account_id: {g.account_id}")
            click.echo(f"  ref:        {g.ref}")

    asyncio.run(run())


@aws_group.command("delete-task-group")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this AWS task group?")
def aws_delete_task_group(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an AWS Route53 task group by ref.

    \b
    REF - WAPI object reference (e.g. awsrte53taskgroup/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.cloud.awsrte53taskgroup.delete(ref)
            click.echo(f"Deleted AWS task group: {ref}")

    asyncio.run(run())


@aws_group.command("list-users")
@_shared_options
@click.option("--account-id", default=None, help="Filter by AWS Account ID.")
def aws_list_users(grid_url, username, password, wapi_ver, verify, account_id):
    """List AWS IAM user credentials."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            filters = {}
            if account_id:
                filters["account_id"] = account_id
            count = 0
            click.echo(f"{'Name':<30} {'Account ID':<20} {'Status':<15} {'Ref'}")
            click.echo("-" * 100)
            async for u in client.cloud.awsuser.list(**filters):
                click.echo(
                    f"{(u.name or '')[:29]:<30} "
                    f"{(u.account_id or ''):<20} "
                    f"{(u.status or ''):<15} "
                    f"{u.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} AWS user(s)")

    asyncio.run(run())


@aws_group.command("create-user")
@_shared_options
@click.option("--name", required=True, help="Display name for the AWS user.")
@click.option("--access-key", required=True, help="AWS Access Key ID.")
@click.option("--secret-key", required=True, hide_input=True, help="AWS Secret Access Key.")
@click.option("--account-id", default=None, help="AWS Account ID.")
@click.option("--comment", default=None, help="Optional comment.")
def aws_create_user(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    access_key,
    secret_key,
    account_id,
    comment,
):
    """Create an AWS IAM user credential entry."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "access_key_id": access_key,
                "secret_access_key": secret_key,
            }
            if account_id:
                payload["account_id"] = account_id
            if comment:
                payload["comment"] = comment
            u = await client.cloud.awsuser.create(payload)
            click.echo(f"Created AWS user: {u.name}")
            click.echo(f"  ref: {u.ref}")

    asyncio.run(run())


# ===========================================================================
# Azure sub-group
# ===========================================================================


@cli.group("azure")
def azure_group():
    """Manage Azure DNS task groups and users."""


@azure_group.command("list-task-groups")
@_shared_options
def azure_list_task_groups(grid_url, username, password, wapi_ver, verify):
    """List Azure DNS task groups."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<30} {'Status':<15} {'Ref'}")
            click.echo("-" * 90)
            async for g in client.cloud.azurednstaskgroup.list():
                click.echo(f"{(g.name or '')[:29]:<30} {(g.sync_status or ''):<15} {g.ref or ''}")
                count += 1
            click.echo(f"\nTotal: {count} Azure task group(s)")

    asyncio.run(run())


@azure_group.command("create-task-group")
@_shared_options
@click.option("--name", required=True, help="Task group name.")
@click.option("--subscription-id", default=None, help="Azure Subscription ID.")
@click.option("--grid-member", default=None, help="Grid member to run tasks on.")
@click.option("--comment", default=None, help="Optional comment.")
@click.option("--disable/--enable", default=False, show_default=True, help="Disable task group.")
def azure_create_task_group(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    subscription_id,
    grid_member,
    comment,
    disable,
):
    """Create an Azure DNS task group."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "disabled": disable}
            if subscription_id:
                payload["subscription_id"] = subscription_id
            if grid_member:
                payload["grid_member"] = grid_member
            if comment:
                payload["comment"] = comment
            g = await client.cloud.azurednstaskgroup.create(payload)
            click.echo(f"Created Azure task group: {g.name}")
            click.echo(f"  ref: {g.ref}")

    asyncio.run(run())


@azure_group.command("delete-task-group")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this Azure task group?")
def azure_delete_task_group(grid_url, username, password, wapi_ver, verify, ref):
    """Delete an Azure DNS task group by ref.

    \b
    REF - WAPI object reference (e.g. azurednstaskgroup/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.cloud.azurednstaskgroup.delete(ref)
            click.echo(f"Deleted Azure task group: {ref}")

    asyncio.run(run())


@azure_group.command("list-users")
@_shared_options
def azure_list_users(grid_url, username, password, wapi_ver, verify):
    """List Azure service principal credentials."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<30} {'Tenant ID':<38} {'Status':<15} {'Ref'}")
            click.echo("-" * 100)
            async for u in client.cloud.azureuser.list():
                click.echo(
                    f"{(u.name or '')[:29]:<30} "
                    f"{(u.model_extra.get('tenant_id') or ''):<38} "
                    f"{(u.model_extra.get('status') or ''):<15} "
                    f"{u.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} Azure user(s)")

    asyncio.run(run())


@azure_group.command("create-user")
@_shared_options
@click.option("--name", required=True, help="Display name for the Azure service principal.")
@click.option("--tenant-id", required=True, help="Azure Tenant (Directory) ID.")
@click.option("--client-id", required=True, help="Azure Application (Client) ID.")
@click.option("--client-secret", required=True, hide_input=True, help="Azure Client Secret.")
@click.option("--comment", default=None, help="Optional comment.")
def azure_create_user(
    grid_url,
    username,
    password,
    wapi_ver,
    verify,
    name,
    tenant_id,
    client_id,
    client_secret,
    comment,
):
    """Create an Azure service principal credential entry."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if comment:
                payload["comment"] = comment
            u = await client.cloud.azureuser.create(payload)
            click.echo(f"Created Azure user: {u.name}")
            click.echo(f"  ref: {u.ref}")

    asyncio.run(run())


# ===========================================================================
# GCP sub-group
# ===========================================================================


@cli.group("gcp")
def gcp_group():
    """Manage GCP DNS task groups and users."""


@gcp_group.command("list-task-groups")
@_shared_options
def gcp_list_task_groups(grid_url, username, password, wapi_ver, verify):
    """List GCP DNS task groups."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<30} {'Status':<15} {'Ref'}")
            click.echo("-" * 90)
            async for g in client.cloud.gcpdnstaskgroup.list():
                click.echo(f"{(g.name or '')[:29]:<30} {(g.sync_status or ''):<15} {g.ref or ''}")
                count += 1
            click.echo(f"\nTotal: {count} GCP task group(s)")

    asyncio.run(run())


@gcp_group.command("create-task-group")
@_shared_options
@click.option("--name", required=True, help="Task group name.")
@click.option("--project-id", default=None, help="GCP Project ID.")
@click.option("--grid-member", default=None, help="Grid member to run tasks on.")
@click.option("--comment", default=None, help="Optional comment.")
@click.option("--disable/--enable", default=False, show_default=True, help="Disable task group.")
def gcp_create_task_group(
    grid_url, username, password, wapi_ver, verify, name, project_id, grid_member, comment, disable
):
    """Create a GCP DNS task group."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {"name": name, "disabled": disable}
            if project_id:
                payload["project_id"] = project_id
            if grid_member:
                payload["grid_member"] = grid_member
            if comment:
                payload["comment"] = comment
            g = await client.cloud.gcpdnstaskgroup.create(payload)
            click.echo(f"Created GCP task group: {g.name}")
            click.echo(f"  ref: {g.ref}")

    asyncio.run(run())


@gcp_group.command("delete-task-group")
@_shared_options
@click.argument("ref")
@click.confirmation_option(prompt="Are you sure you want to delete this GCP task group?")
def gcp_delete_task_group(grid_url, username, password, wapi_ver, verify, ref):
    """Delete a GCP DNS task group by ref.

    \b
    REF - WAPI object reference (e.g. gcpdnstaskgroup/ZG5z...)
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            await client.cloud.gcpdnstaskgroup.delete(ref)
            click.echo(f"Deleted GCP task group: {ref}")

    asyncio.run(run())


@gcp_group.command("list-users")
@_shared_options
def gcp_list_users(grid_url, username, password, wapi_ver, verify):
    """List GCP service account credentials."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Name':<30} {'Account Email':<45} {'Ref'}")
            click.echo("-" * 100)
            async for u in client.cloud.gcpuser.list():
                click.echo(
                    f"{(u.name or '')[:29]:<30} "
                    f"{(u.model_extra.get('service_account_email') or ''):<45} "
                    f"{u.ref or ''}"
                )
                count += 1
            click.echo(f"\nTotal: {count} GCP user(s)")

    asyncio.run(run())


@gcp_group.command("create-user")
@_shared_options
@click.option("--name", required=True, help="Display name for the GCP service account.")
@click.option("--account-email", required=True, help="GCP service account email address.")
@click.option("--comment", default=None, help="Optional comment.")
def gcp_create_user(grid_url, username, password, wapi_ver, verify, name, account_email, comment):
    """Create a GCP service account credential entry.

    Note: the service account key JSON file must be uploaded separately
    via fileop uploadinit before referencing the token here.
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            payload = {
                "name": name,
                "service_account_email": account_email,
            }
            if comment:
                payload["comment"] = comment
            u = await client.cloud.gcpuser.create(payload)
            click.echo(f"Created GCP user: {u.name}")
            click.echo(f"  ref: {u.ref}")

    asyncio.run(run())


# ===========================================================================
# Multi-regions
# ===========================================================================


@cli.command("list-multiregions")
@_shared_options
def list_multiregions_cmd(grid_url, username, password, wapi_ver, verify):
    """List configured cloud multi-region definitions."""

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            count = 0
            click.echo(f"{'Ref':<60} {'Details'}")
            click.echo("-" * 100)
            async for mr in client.cloud.multiregions.list():
                details = str(mr.model_extra) if mr.model_extra else ""
                click.echo(f"{(mr.ref or ''):<60} {details[:60]}")
                count += 1
            click.echo(f"\nTotal: {count} multi-region config(s)")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
