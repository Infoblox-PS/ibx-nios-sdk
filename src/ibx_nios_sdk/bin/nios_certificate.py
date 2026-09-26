#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024-2026 Infoblox, Inc.
"""nios_certificate - Upload or download NIOS SSL certificates via the WAPI fileop endpoint.

This CLI utility authenticates against an Infoblox Grid Manager and either
uploads a certificate file (using ``uploadinit`` + PUT + ``uploadcertificate``)
or downloads a certificate (using ``downloadcertificate``).

Usage examples::

    nios_certificate upload -g 192.168.1.2 -m gm.example.com -f server.pem
    nios_certificate download -g 192.168.1.2 -m gm.example.com -f cert_out.pem

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

logger = logging.getLogger("nios_certificate")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)

CERT_USAGES = ["ADMIN", "CAPTIVE_PORTAL", "SFNT_CLIENT_CERT", "IFMAP_DHCP", "EAP_CA", "TAE_CA"]

help_text = """
Upload or download NIOS SSL certificates via the WAPI fileop endpoint.
"""


@click.group(
    help=help_text,
    context_settings=dict(max_content_width=95, help_option_names=["-h", "--help"]),
)
def main() -> None:
    """NIOS SSL Certificate Tools."""
    pass


@main.command()
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option("-m", "--member", required=True, help="Grid member hostname for the certificate")
@optgroup.option("-f", "--filename", required=True, help="Local certificate file path to upload")
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
    "--cert-type",
    type=click.Choice(CERT_USAGES, case_sensitive=True),
    default="ADMIN",
    show_default=True,
    help="Certificate usage type",
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
def upload(
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    cert_type: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Upload a certificate file to an Infoblox Grid member.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Grid member hostname to associate the certificate with.
        filename: Local certificate file path (PEM format).
        username: WAPI username for authentication.
        cert_type: Certificate usage type (e.g. ``ADMIN``, ``CAPTIVE_PORTAL``).
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the upload operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    asyncio.run(
        _run_upload(
            grid_mgr=grid_mgr,
            member=member,
            filename=filename,
            username=username,
            cert_type=cert_type,
            wapi_ver=wapi_ver,
        )
    )


@main.command()
@optgroup.group("Required Parameters")
@optgroup.option("-g", "--grid-mgr", required=True, help="Infoblox Grid Manager hostname or URL")
@optgroup.option("-m", "--member", required=True, help="Grid member hostname for the certificate")
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
    default="certificate.pem",
    show_default=True,
    help="Output file path to write the downloaded certificate",
)
@optgroup.option(
    "-t",
    "--cert-type",
    type=click.Choice(
        ["ADMIN", "CAPTIVE_PORTAL", "SFNT_CLIENT_CERT", "IFMAP_DHCP"], case_sensitive=True
    ),
    default="ADMIN",
    show_default=True,
    help="Certificate usage type",
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
def download(
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    cert_type: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """Download a certificate from an Infoblox Grid member.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Grid member hostname to retrieve the certificate from.
        filename: Local file path where the certificate will be written.
        username: WAPI username for authentication.
        cert_type: Certificate usage type (e.g. ``ADMIN``, ``CAPTIVE_PORTAL``).
        wapi_ver: WAPI version string to use (e.g. ``"2.14"``).
        debug: When True, sets logging to DEBUG level.

    Returns:
        None

    Raises:
        NiosError: If authentication or the download operation fails.
        SystemExit: Always raised on completion or error.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    asyncio.run(
        _run_download(
            grid_mgr=grid_mgr,
            member=member,
            filename=filename,
            username=username,
            cert_type=cert_type,
            wapi_ver=wapi_ver,
        )
    )


async def _run_upload(
    *,
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    cert_type: str,
    wapi_ver: str,
) -> None:
    """Async implementation of the certificate upload workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Grid member hostname to associate the certificate with.
        filename: Local certificate file path.
        username: WAPI username for authentication.
        cert_type: Certificate usage type.
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

            # Step 1: Initiate upload session
            init_result = await client.misc.fileop.upload_init()
            token = init_result.get("token")
            upload_url = init_result.get("url")

            if not token or not upload_url:
                logger.error("uploadinit response missing token or url: %s", init_result)
                sys.exit(1)

            logger.info("Upload session initiated; uploading certificate %s", filename)

            # Step 2: PUT the certificate file
            with open(filename, "rb") as fh:
                cert_data = fh.read()

            upload_response = await client._http._client.put(
                upload_url,
                content=cert_data,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_response.raise_for_status()
            logger.info("Certificate file uploaded")

            # Step 3: Associate the certificate with the member
            await client.misc.fileop.upload_certificate(
                token=token,
                member=member,
                usage=cert_type,
            )
            logger.info(
                "Certificate uploaded successfully for member %s (type=%s)", member, cert_type
            )

    except NiosError as err:
        logger.error(err)
        sys.exit(1)
    except OSError as err:
        logger.error("Failed to read certificate file %s: %s", filename, err)
        sys.exit(1)

    sys.exit(0)


async def _run_download(
    *,
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    cert_type: str,
    wapi_ver: str,
) -> None:
    """Async implementation of the certificate download workflow.

    Args:
        grid_mgr: Hostname or full URL of the Infoblox Grid Manager.
        member: Grid member hostname to retrieve the certificate from.
        filename: Local file path where the certificate will be written.
        username: WAPI username for authentication.
        cert_type: Certificate usage type.
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

            # Request the certificate download token and URL
            result = await client.misc.fileop.downloadcertificate(
                member=member,
                certificate_usage=cert_type,
            )
            token = result.get("token")
            download_url = result.get("url")

            if not token or not download_url:
                logger.error("downloadcertificate response missing token or url: %s", result)
                sys.exit(1)

            logger.info("Certificate download initiated; saving to %s", filename)

            # Stream the certificate to disk
            async with client._http._client.stream("GET", download_url) as response:
                response.raise_for_status()
                with open(filename, "wb") as fh:
                    async for chunk in response.aiter_bytes(chunk_size=65536):
                        fh.write(chunk)

            logger.info("Certificate saved to %s", filename)

            # Acknowledge the download
            await client.misc.fileop.download_complete(token=token)
            logger.info("Download acknowledged successfully")

    except NiosError as err:
        logger.error(err)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
