#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_csvimport - Import a local CSV file into NIOS via the WAPI fileop endpoint.

This CLI utility authenticates against an Infoblox Grid Manager, uploads a CSV
file using the WAPI ``uploadinit`` / HTTP PUT flow, then triggers the
``csv_import`` fileop function to load the data.  The import task ID is printed
so the operator can track progress via the WAPI ``csvimporttask`` object.

Usage example::

    nios_csvimport -g 192.168.1.2 -f networks.csv -o MERGE

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
from pathlib import Path

import click
from click_option_group import optgroup

from ibx_nios_sdk import NiosClient, NiosError

log = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

_IMPORT_OPERATIONS = ["INSERT", "OVERRIDE", "MERGE", "DELETE", "CUSTOM"]

help_text = """
Import a CSV file into NIOS via the fileop uploadinit / csv_import flow.
"""


@click.command(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option("-f", "--filename", required=True, help="Local CSV file path to upload")
@optgroup.option(
    "-o",
    "--operation",
    required=True,
    type=click.Choice(_IMPORT_OPERATIONS, case_sensitive=False),
    help="CSV import operation: INSERT | OVERRIDE | MERGE | DELETE | CUSTOM",
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
    operation: str,
    username: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Import a CSV file into NIOS via the fileop endpoint.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        filename: Local path to the CSV file to be imported.
        operation: Import operation mode (INSERT, OVERRIDE, MERGE, DELETE, CUSTOM).
        username: WAPI username for authentication.
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the import operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        log.setLevel(logging.DEBUG)

    asyncio.run(
        _run(
            grid_mgr=grid_mgr,
            filename=filename,
            operation=operation.upper(),
            username=username,
            wapi_ver=wapi_ver,
        )
    )


async def _run(
    *, grid_mgr: str, filename: str, operation: str, username: str, wapi_ver: str
) -> None:
    """Async implementation of the CSV import workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        filename: Local path to the CSV file to be imported.
        operation: Import operation mode string.
        username: WAPI username for authentication.
        wapi_ver: WAPI version string to use.

    Returns:
        None

    Raises:
        SystemExit: On error or completion.
    """
    csv_path = Path(filename)
    if not csv_path.is_file():
        log.error("File not found: %s", filename)
        sys.exit(1)

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

            # Step 1: initialise an upload session
            init_result = await client.misc.fileop.upload_init()
            token = init_result.get("token")
            upload_url = init_result.get("url")

            if not token or not upload_url:
                log.error("uploadinit response missing token or url: %s", init_result)
                sys.exit(1)

            log.info("Upload session initialised; uploading %s", filename)

            # Step 2: PUT the CSV file content to the upload URL
            csv_data = csv_path.read_bytes()
            put_response = await client._http._client.put(
                upload_url,
                content=csv_data,
                headers={"Content-Type": "application/octet-stream"},
            )
            put_response.raise_for_status()
            log.info("File uploaded successfully (%d bytes)", len(csv_data))

            # Step 3: trigger the CSV import using the upload token
            import_result = await client.misc.fileop.csv_import(
                token=token,
                action="START",
                on_error="STOP",
                operation=operation,
            )
            import_id = import_result.get("import_id") or import_result.get("_ref", "")
            log.info("CSV import started - import_id: %s", import_id)
            log.info("Monitor progress via: GET /csvimporttask?import_id=%s", import_id)

    except NiosError as err:
        log.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
