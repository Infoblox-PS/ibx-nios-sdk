#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_grid_restore - Upload and restore an Infoblox NIOS Grid backup.

This CLI utility authenticates against an Infoblox Grid Manager, uploads a
local backup file using the WAPI fileop upload workflow (``uploadinit`` + PUT),
and then triggers a Grid restore via the ``restoredatabase`` fileop function.

Usage example::

    nios_grid_restore -g 192.168.1.2 -f database.bak
    nios_grid_restore -g 192.168.1.2 -f database.bak -r FORCED -k

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

logger = logging.getLogger("nios_grid_restore")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

help_text = """
Upload a local backup file and restore the NIOS Grid via the fileop restoredatabase endpoint.
"""


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option("-f", "--filename", required=True, help="Local backup file path to upload")
@optgroup.group("Optional Parameters")
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    show_default=True,
    help="Infoblox admin username",
)
@optgroup.option(
    "-r",
    "--restore-mode",
    type=click.Choice(["NORMAL", "FORCED", "CLONE"], case_sensitive=True),
    default="NORMAL",
    show_default=True,
    help="Grid restore mode",
)
@optgroup.option(
    "-k",
    "--keep",
    is_flag=True,
    help="Keep existing Grid IP rather than using the IP from the backup",
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
    filename: str,
    username: str,
    restore_mode: str,
    keep: bool,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Upload a backup and restore the NIOS Grid.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        filename: Local backup file path to upload and restore from.
        username: WAPI username for authentication.
        restore_mode: Restore mode - ``NORMAL``, ``FORCED``, or ``CLONE``.
        keep: When True, keep the existing Grid IP instead of the backup IP.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the restore operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    asyncio.run(
        _run(
            grid_mgr=grid_mgr,
            filename=filename,
            username=username,
            restore_mode=restore_mode,
            keep=keep,
            wapi_ver=wapi_ver,
        )
    )


async def _run(
    *,
    grid_mgr: str,
    filename: str,
    username: str,
    restore_mode: str,
    keep: bool,
    wapi_ver: str,
) -> None:
    """Async implementation of the Grid restore workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        filename: Local backup file path to upload.
        username: WAPI username for authentication.
        restore_mode: Restore mode (``NORMAL``, ``FORCED``, or ``CLONE``).
        keep: When True, retain the existing Grid IP address.
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

            # Step 1: Initiate upload session - returns {"token": "...", "url": "..."}
            init_result = await client.misc.fileop.upload_init()
            token = init_result.get("token")
            upload_url = init_result.get("url")

            if not token or not upload_url:
                logger.error("uploadinit response missing token or url: %s", init_result)
                sys.exit(1)

            logger.info("Upload session initiated; uploading %s", filename)

            # Step 2: PUT the backup file to the upload URL
            with open(filename, "rb") as fh:
                file_data = fh.read()

            upload_response = await client._http._client.put(
                upload_url,
                content=file_data,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_response.raise_for_status()
            logger.info("File uploaded successfully")

            # Step 3: Trigger the restore
            logger.info("Initiating restore with mode=%s, keep_grid_ip=%s", restore_mode, keep)
            await client.misc.fileop.call(
                "restoredatabase",
                mode=restore_mode,
                keep_grid_ip=keep,
                token=token,
            )
            logger.info("Grid restore initiated successfully")

    except NiosError as err:
        logger.error(err)
        sys.exit(1)
    except OSError as err:
        logger.error("Failed to read backup file %s: %s", filename, err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
