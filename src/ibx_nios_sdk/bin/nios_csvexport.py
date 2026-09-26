#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_csvexport - Export NIOS WAPI objects to a local CSV file.

This CLI utility authenticates against an Infoblox Grid Manager and exports
a chosen WAPI object type (e.g. ``network``, ``record:a``) to a CSV file using
the WAPI fileop ``csv_export`` function.  The export token is acknowledged with
``downloadcomplete`` after the file is written to disk.

Usage example::

    nios_csvexport -g 192.168.1.2 -f networks.csv -o network

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

log = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

help_text = """
Export NIOS WAPI objects to a CSV file via the fileop csv_export endpoint.
"""


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option("-f", "--filename", required=True, help="Output CSV file path to write")
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
@optgroup.option(
    "-o",
    "--obj",
    default="network",
    show_default=True,
    help="WAPI object type to export (e.g. network, record:a)",
)
@optgroup.group("Logging Parameters")
@optgroup.option("--debug", is_flag=True, help="Enable verbose debug logging")
def main(
    grid_mgr: str,
    filename: str,
    username: str,
    wapi_ver: str,
    obj: str,
    debug: bool,
) -> None:
    """Export NIOS WAPI objects to a CSV file.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        filename: Local file path where the exported CSV will be written.
        username: WAPI username for authentication.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        obj: WAPI object type to export (e.g. ``"network"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the export operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

    asyncio.run(
        _run(grid_mgr=grid_mgr, filename=filename, username=username, wapi_ver=wapi_ver, obj=obj)
    )


async def _run(*, grid_mgr: str, filename: str, username: str, wapi_ver: str, obj: str) -> None:
    """Async implementation of the CSV export workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        filename: Local file path where the exported CSV will be written.
        username: WAPI username for authentication.
        wapi_ver: WAPI version string to use.
        obj: WAPI object type to export.

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
            log.info("Connected to Infoblox Grid Manager %s", grid_url)

            # Initiate CSV export - returns {"token": "...", "url": "..."}
            result = await client.misc.fileop.csv_export(_object=obj)
            token = result.get("token")
            download_url = result.get("url")

            if not token or not download_url:
                log.error("csv_export response missing token or url: %s", result)
                sys.exit(1)

            log.info("CSV export initiated; downloading to %s", filename)

            # Download the file using the shared httpx session (cookie still valid)
            async with client._http._client.stream("GET", download_url) as response:
                response.raise_for_status()
                with open(filename, "wb") as fh:
                    async for chunk in response.aiter_bytes(chunk_size=65536):
                        fh.write(chunk)

            log.info("Download complete - saved to %s", filename)

            # Acknowledge the download so NIOS can clean up the export session
            await client.misc.fileop.download_complete(token=token)
            log.info("Download acknowledged successfully")

    except NiosError as err:
        log.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
