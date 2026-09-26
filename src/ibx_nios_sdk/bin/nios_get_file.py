#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_get_file - Download a NIOS configuration file from a Grid member.

This CLI utility authenticates against an Infoblox Grid Manager and retrieves
a member configuration file (e.g. ``DNS_CFG``, ``DHCP_CFG``) via the WAPI
fileop ``getfile`` function.  The file is written to the path given by
``--filename``.

Usage example::

    nios_get_file -g 192.168.1.2 -m ns1.example.com -f dns_cfg.txt

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

_CONFIG_TYPES = [
    "DNS_CACHE",
    "DNS_CFG",
    "DHCP_CFG",
    "DHCPV6_CFG",
    "TRAFFIC_CAPTURE_FILE",
    "DNS_STATS",
    "DNS_RECURSING_CACHE",
]

help_text = """
Download a NIOS member configuration file via the fileop getfile endpoint.
"""


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option(
    "-m", "--member", required=True, help="Grid member hostname to retrieve file from"
)
@optgroup.option(
    "-f", "--filename", required=True, help="Output file path to write the downloaded file"
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
    "-t",
    "--cfg-type",
    default="DNS_CFG",
    show_default=True,
    type=click.Choice(_CONFIG_TYPES, case_sensitive=False),
    help=(
        "Configuration type: DNS_CACHE | DNS_CFG | DHCP_CFG | DHCPV6_CFG"
        " | TRAFFIC_CAPTURE_FILE | DNS_STATS | DNS_RECURSING_CACHE"
    ),
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
    member: str,
    filename: str,
    username: str,
    cfg_type: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Download a NIOS member configuration file.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Fully-qualified hostname of the Grid member to query.
        filename: Local path where the downloaded file will be written.
        username: WAPI username for authentication.
        cfg_type: Configuration file type (e.g. ``"DNS_CFG"``).
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the file retrieval fails.
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
            cfg_type=cfg_type.upper(),
            wapi_ver=wapi_ver,
        )
    )


async def _run(
    *, grid_mgr: str, member: str, filename: str, username: str, cfg_type: str, wapi_ver: str
) -> None:
    """Async implementation of the getfile download workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Fully-qualified hostname of the Grid member.
        filename: Local path where the file will be written.
        username: WAPI username for authentication.
        cfg_type: Configuration file type string.
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

            # Request the file - WAPI returns a token + download URL
            result = await client.misc.fileop.call(
                "getfile",
                member=member,
                type=cfg_type,
            )
            token = result.get("token")
            download_url = result.get("url")

            if not token or not download_url:
                log.error("getfile response missing token or url: %s", result)
                sys.exit(1)

            log.info("File ready; downloading %s/%s to %s", member, cfg_type, filename)

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
