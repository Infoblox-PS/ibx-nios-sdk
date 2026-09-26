#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_get_log - Download a Grid member log file from NIOS.

This CLI utility authenticates against an Infoblox Grid Manager and downloads
a member log (e.g. ``SYSLOG``, ``AUDITLOG``) via the WAPI fileop
``get_log_files`` function.  The log content is written to a local file.

Usage example::

    nios_get_log -g 192.168.1.2 -m ns1.example.com -f syslog.txt
    nios_get_log -g 192.168.1.2 -m ns1.example.com -l AUDITLOG -f audit.txt

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

_LOG_TYPES = [
    "SYSLOG",
    "AUDITLOG",
    "MSMGMTLOG",
    "DELTALOG",
    "OUTBOUND",
    "PTOPLOG",
    "DISCOVERY_CSV_ERRLOG",
]

help_text = """
Download a NIOS Grid member log file via the fileop get_log_files endpoint.
"""


class _LogTypeParam(click.ParamType[str]):
    """Case-insensitive log-type choice that normalises to upper case."""

    name = "log_type"

    def convert(self, value: str, param: click.Parameter | None, ctx: click.Context | None) -> str:
        """Convert and validate the log type value.

        Args:
            value: Raw CLI string value entered by the user.
            param: Click parameter object being converted.
            ctx: Click context for the current command invocation.

        Returns:
            The validated log type string, normalised to upper case.

        Raises:
            click.BadParameter: If ``value`` is not a recognised log type.
        """
        upper = value.upper()
        if upper in _LOG_TYPES:
            return upper
        self.fail(
            f"{value!r} is not a valid log type. Choose from: {', '.join(_LOG_TYPES)}",
            param,
            ctx,
        )
        return upper  # unreachable; satisfies type checker


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option("-m", "--member", required=True, help="Grid member hostname to retrieve log from")
@optgroup.option(
    "-f", "--filename", required=True, help="Output file path to write the downloaded log"
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
    "-l",
    "--log-type",
    default="SYSLOG",
    show_default=True,
    type=_LogTypeParam(),
    help=(
        "Log type to retrieve: SYSLOG | AUDITLOG | MSMGMTLOG | DELTALOG"
        " | OUTBOUND | PTOPLOG | DISCOVERY_CSV_ERRLOG"
    ),
)
@optgroup.option(
    "-n",
    "--node-type",
    default="ACTIVE",
    show_default=True,
    type=click.Choice(["ACTIVE", "BACKUP"], case_sensitive=False),
    help="HA node to retrieve the log from: ACTIVE | BACKUP",
)
@optgroup.option(
    "-r",
    "--rotated-logs",
    is_flag=True,
    help="Include rotated log files (only valid when --log-type is SYSLOG)",
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
    log_type: str,
    node_type: str,
    rotated_logs: bool,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Download a NIOS Grid member log file.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Fully-qualified hostname of the Grid member to query.
        filename: Local path where the downloaded log will be written.
        username: WAPI username for authentication.
        log_type: Log type to retrieve (e.g. ``"SYSLOG"``).
        node_type: HA node type (``"ACTIVE"`` or ``"BACKUP"``).
        rotated_logs: When True, include rotated log files (SYSLOG only).
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the log retrieval fails.
        SystemExit: Always raised on completion or error.
    """
    if rotated_logs and log_type != "SYSLOG":
        raise click.BadParameter("--rotated-logs can only be set when --log-type is SYSLOG")

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

    asyncio.run(
        _run(
            grid_mgr=grid_mgr,
            member=member,
            filename=filename,
            username=username,
            log_type=log_type,
            node_type=node_type.upper(),
            rotated_logs=rotated_logs,
            wapi_ver=wapi_ver,
        )
    )


async def _run(
    *,
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    log_type: str,
    node_type: str,
    rotated_logs: bool,
    wapi_ver: str,
) -> None:
    """Async implementation of the log download workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Fully-qualified hostname of the Grid member.
        filename: Local path where the log file will be written.
        username: WAPI username for authentication.
        log_type: Log type string (e.g. ``"SYSLOG"``).
        node_type: HA node type string (``"ACTIVE"`` or ``"BACKUP"``).
        rotated_logs: Whether to include rotated log files.
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

            # Request the log file - WAPI returns token + download URL
            result = await client.misc.fileop.call(
                "get_log_files",
                member=member,
                log_type=log_type,
                node_type=node_type,
                include_rotated=rotated_logs,
            )
            token = result.get("token")
            download_url = result.get("url")

            if not token or not download_url:
                log.error("get_log_files response missing token or url: %s", result)
                sys.exit(1)

            log.info("Log ready; downloading %s/%s to %s", member, log_type, filename)

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
