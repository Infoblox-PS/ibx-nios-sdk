#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_restart_status - List NIOS service restart status for all Grid members.

This CLI utility authenticates against an Infoblox Grid Manager and displays
the current restart status (DNS, DHCP, reporting) for every Grid member in a
tabular format.

Usage example::

    nios_restart_status -g 192.168.1.2

Copyright 2024-2026 Infoblox, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import asyncio
import getpass
import logging
import os
import sys

import click
from click_option_group import optgroup

from ibx_nios_sdk import NiosClient, NiosError

logger = logging.getLogger("nios_restart_status")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

help_text = """
Display the NIOS service restart status for all Grid members in a tabular format.
"""


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.group("Optional Parameters")
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    show_default=True,
    help="Infoblox admin username",
)
@optgroup.option(
    "-w",
    "--wapi-ver",
    default="2.14",
    show_default=True,
    help="Infoblox WAPI version",
)
@optgroup.group("Logging Parameters")
@optgroup.option("--debug", is_flag=True, help="Enable verbose debug logging")
def main(
    grid_mgr: str,
    username: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """List NIOS service restart status.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        username: WAPI username for authentication.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the status query fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    asyncio.run(_run(grid_mgr=grid_mgr, username=username, wapi_ver=wapi_ver))


async def _run(*, grid_mgr: str, username: str, wapi_ver: str) -> None:
    """Async implementation of the restart status listing workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        username: WAPI username for authentication.
        wapi_ver: WAPI version string to use.

    Returns:
        None

    Raises:
        SystemExit: On error or completion.
    """
    grid_url = grid_mgr if grid_mgr.startswith("http") else f"https://{grid_mgr}"
    password = os.environ.get("NIOS_PASSWORD") or getpass.getpass(
        f"Enter password for [{username}]: "
    )

    try:
        async with NiosClient(
            grid_url=grid_url,
            username=username,
            password=password,
            wapi_version=wapi_ver,
            verify=False,
        ) as client:
            logger.info("Connected to Infoblox Grid Manager %s", grid_url)

            statuses = await client.grid.restartservicestatus.list().all()

            if not statuses:
                click.echo("No restart service status records found.")
                sys.exit(0)

            # Print tabular output
            col_w = 30
            header = (
                f"{'Member':<{col_w}}  {'DNS Status':<20}  "
                f"{'DHCP Status':<20}  {'Reporting Status':<20}"
            )
            separator = "-" * len(header)
            click.echo(separator)
            click.echo(header)
            click.echo(separator)

            for status in statuses:
                member = status.member or "unknown"
                dns = status.dns_status or "N/A"
                dhcp = status.dhcp_status or "N/A"
                reporting = status.reporting_status or "N/A"
                click.echo(f"{member:<{col_w}}  {dns:<20}  {dhcp:<20}  {reporting:<20}")

            click.echo(separator)
            click.echo(f"Total: {len(statuses)} member(s)")

    except NiosError as err:
        logger.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
