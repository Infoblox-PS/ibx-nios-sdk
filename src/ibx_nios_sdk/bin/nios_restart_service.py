#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_restart_service - Restart NIOS protocol services on a Grid or member.

This CLI utility authenticates against an Infoblox Grid Manager and restarts
the specified services either grid-wide (default) or on a specific member.

Usage examples::

    nios_restart_service -g 192.168.1.2
    nios_restart_service -g 192.168.1.2 -s DNS -s DHCP
    nios_restart_service -g 192.168.1.2 -m member.example.com -s DNS

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

logger = logging.getLogger("nios_restart_service")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

help_text = """
Restart NIOS protocol services on the entire Grid or on a specific member.

When --member is omitted the restart is applied grid-wide using the Grid object.
When --member is supplied only that member is restarted.
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
    "-m",
    "--member",
    default=None,
    help="Specific Grid member hostname to restart (omit for grid-wide restart)",
)
@optgroup.option(
    "-s",
    "--services",
    multiple=True,
    default=["DNS", "DHCP"],
    show_default=True,
    help="Service(s) to restart - may be repeated (e.g. -s DNS -s DHCP)",
)
@optgroup.option(
    "-r",
    "--restart-option",
    type=click.Choice(
        ["RESTART_IF_NEEDED", "FORCE_RESTART", "RELOAD_ALL", "RESTART_ALL"],
        case_sensitive=True,
    ),
    default="RESTART_IF_NEEDED",
    show_default=True,
    help="Restart trigger policy",
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
    member: str | None,
    services: tuple[str, ...],
    restart_option: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Restart NIOS protocol services.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        username: WAPI username for authentication.
        member: Optional member hostname. When provided only that member is
            restarted; when absent the restart is applied grid-wide.
        services: Tuple of service names to restart (e.g. ``("DNS", "DHCP")``).
        restart_option: Restart trigger policy.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the restart operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    asyncio.run(
        _run(
            grid_mgr=grid_mgr,
            username=username,
            member=member,
            services=list(services),
            restart_option=restart_option,
            wapi_ver=wapi_ver,
        )
    )


async def _run(
    *,
    grid_mgr: str,
    username: str,
    member: str | None,
    services: list[str],
    restart_option: str,
    wapi_ver: str,
) -> None:
    """Async implementation of the service restart workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        username: WAPI username for authentication.
        member: Optional member hostname.
        services: List of service names to restart.
        restart_option: Restart trigger policy.
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

            if member:
                # Restart services on a specific member
                member_obj = await client.grid.member.find_one(host_name=member)
                if not member_obj:
                    logger.error("Member %r not found in the Grid", member)
                    sys.exit(1)

                if member_obj.ref is None:
                    logger.error("Member %r has no WAPI reference", member)
                    sys.exit(1)
                await client.grid.member.restart_services(
                    member_obj.ref,
                    services=services,
                    restart_option=restart_option,
                )
                logger.info(
                    "Restarted services %s on member %s (option=%s)",
                    services,
                    member,
                    restart_option,
                )
            else:
                # Grid-wide restart - fetch the Grid object ref
                grids = await client.grid.grid.list().all()
                if not grids:
                    logger.error("No Grid object found")
                    sys.exit(1)

                grid_ref = grids[0].ref
                if grid_ref is None:
                    logger.error("Grid object has no WAPI reference")
                    sys.exit(1)
                await client.grid.grid.restart_services(
                    grid_ref,
                    services=services,
                    restart_option=restart_option,
                )
                logger.info(
                    "Restarted services %s grid-wide (option=%s)",
                    services,
                    restart_option,
                )

    except NiosError as err:
        logger.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
