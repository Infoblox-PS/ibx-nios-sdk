#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_get_supportbundle - Download a NIOS Grid member support bundle.

This CLI utility authenticates against an Infoblox Grid Manager and retrieves
a support bundle from a specified Grid member via the WAPI fileop
``get_support_bundle`` function.  The bundle is written to a local file.

Usage example::

    nios_get_supportbundle -g 192.168.1.2 -m ns1.example.com -f bundle.tar.gz
    nios_get_supportbundle -g 192.168.1.2 -m ns1.example.com -f bundle.tar.gz -r -l

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
Download a support bundle from a NIOS Grid member via the fileop get_support_bundle endpoint.
"""


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option(
    "-m", "--member", required=True, help="Grid member hostname to retrieve bundle from"
)
@optgroup.option(
    "-f", "--filename", required=True, help="Output file path to write the support bundle"
)
@optgroup.group("Optional Parameters")
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    show_default=True,
    help="Infoblox admin username",
)
@optgroup.option(
    "-r", "--rotated-logs", is_flag=True, help="Include rotated log files in the bundle"
)
@optgroup.option("-l", "--log-files", is_flag=True, help="Include log files in the bundle")
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
    member: str,
    filename: str,
    username: str,
    rotated_logs: bool,
    log_files: bool,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Download a NIOS Grid member support bundle.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Fully-qualified hostname of the Grid member to query.
        filename: Local path where the support bundle will be written.
        username: WAPI username for authentication.
        rotated_logs: When True, include rotated log files in the bundle.
        log_files: When True, include current log files in the bundle.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the bundle retrieval fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

    asyncio.run(
        _run(
            grid_mgr=grid_mgr,
            member=member,
            filename=filename,
            username=username,
            rotated_logs=rotated_logs,
            log_files=log_files,
            wapi_ver=wapi_ver,
        )
    )


async def _run(
    *,
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    rotated_logs: bool,
    log_files: bool,
    wapi_ver: str,
) -> None:
    """Async implementation of the support bundle download workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Fully-qualified hostname of the Grid member.
        filename: Local path where the bundle will be written.
        username: WAPI username for authentication.
        rotated_logs: Whether to include rotated log files.
        log_files: Whether to include current log files.
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
            log.info("Connected to Infoblox Grid Manager %s", grid_url)

            # Request the support bundle - WAPI returns token + download URL
            result = await client.misc.fileop.call(
                "get_support_bundle",
                member=member,
                log_files=log_files,
                nm_snmp_logs=False,
                recursive_cache_file=False,
                rotate_log_files=rotated_logs,
            )
            token = result.get("token")
            download_url = result.get("url")

            if not token or not download_url:
                log.error("get_support_bundle response missing token or url: %s", result)
                sys.exit(1)

            log.info("Support bundle ready; downloading for member %s to %s", member, filename)

            # Stream the download using the shared httpx session
            async with client._http._client.stream("GET", download_url) as response:
                response.raise_for_status()
                with open(filename, "wb") as fh:
                    async for chunk in response.aiter_bytes(chunk_size=65536):
                        fh.write(chunk)

            log.info("Download complete - saved to %s", filename)

            # Acknowledge the download
            await client.misc.fileop.download_complete(token=token)
            log.info("Download acknowledged successfully")

    except NiosError as err:
        log.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
