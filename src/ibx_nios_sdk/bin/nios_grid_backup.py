#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_grid_backup - Download an Infoblox NIOS Grid backup to a local file.

This CLI utility authenticates against an Infoblox Grid Manager and downloads
a full Grid backup using the WAPI fileop ``getgriddata`` function.  After the
binary file is written to disk the download session is acknowledged with
``downloadcomplete``.

Usage example::

    nios_grid_backup -g 192.168.1.2 -f database.bak

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

logger = logging.getLogger("nios_grid_backup")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

help_text = """
Download a full NIOS Grid backup to a local file via the fileop getgriddata endpoint.
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
    "-f",
    "--filename",
    default="database.bak",
    show_default=True,
    help="Output file path to write the backup",
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
    filename: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Download a NIOS Grid backup to a local file.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        username: WAPI username for authentication.
        filename: Local file path where the backup will be written.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the backup operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    asyncio.run(_run(grid_mgr=grid_mgr, username=username, filename=filename, wapi_ver=wapi_ver))


async def _run(*, grid_mgr: str, username: str, filename: str, wapi_ver: str) -> None:
    """Async implementation of the Grid backup download workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        username: WAPI username for authentication.
        filename: Local file path where the backup will be written.
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

            # Initiate the backup - returns {"token": "...", "url": "..."}
            result = await client.misc.fileop.call("getgriddata", type="BACKUP")
            token = result.get("token")
            download_url = result.get("url")

            if not token or not download_url:
                logger.error("getgriddata response missing token or url: %s", result)
                sys.exit(1)

            logger.info("Grid backup initiated; downloading to %s", filename)

            # Stream the backup file using the shared httpx session
            async with client._http._client.stream("GET", download_url) as response:
                response.raise_for_status()
                with open(filename, "wb") as fh:
                    async for chunk in response.aiter_bytes(chunk_size=65536):
                        fh.write(chunk)

            logger.info("Download complete - saved to %s", filename)

            # Acknowledge download so NIOS can clean up the session
            await client.misc.fileop.download_complete(token=token)
            logger.info("Download acknowledged successfully")

    except NiosError as err:
        logger.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
