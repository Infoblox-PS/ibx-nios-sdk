# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NIOS Fileop special workflows - CSV import/export round-trips, support bundles, logs, certs.

The NIOS WAPI ``fileop`` resource is function-only (no CRUD). Every operation
is a multi-step workflow: initiate → transfer file → acknowledge completion.
This script demonstrates the full round-trip for each operation.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as fallbacks):
    NIOS_GRID_URL        - Grid manager URL (e.g. https://grid.example.com)
    NIOS_USERNAME        - Admin username
    NIOS_PASSWORD        - Admin password
    NIOS_WAPI_VERSION    - Optional; default 2.14

Examples:
    # --- CSV Export (full round-trip: export → download → ack) ---
    python manage_fileop.py csv-export --object network --output networks.csv
    python manage_fileop.py csv-export --object record:host --output hosts.csv

    # --- CSV Import (full round-trip: init → upload → start import) ---
    python manage_fileop.py csv-import --object network --input networks.csv
    python manage_fileop.py csv-import --object record:host --input hosts.csv --operation MERGE

    # --- Support Bundle ---
    python manage_fileop.py support-bundle --member "infoblox.localdomain" --output support.tgz

    # --- Global Search ---
    python manage_fileop.py search "192.168.1"
    python manage_fileop.py search "example.com" --max-results 50

    # --- Log File Download ---
    python manage_fileop.py get-log --member "infoblox.localdomain" --log-type SYSLOG --output syslog.log

    # --- Certificate Download ---
    python manage_fileop.py get-cert --cert-type HTTPS --output grid_https.pem
    python manage_fileop.py get-cert --cert-type HTTPS --member "infoblox.localdomain" --output member_https.pem
"""

import asyncio

import click

from ibx_nios_sdk import NiosClient


def _connect(grid_url, username, password, wapi_ver, verify):
    return NiosClient(
        grid_url=grid_url,
        username=username,
        password=password,
        wapi_version=wapi_ver,
        verify=verify,
    )


def _shared_options(f):
    """Decorator that adds common connection options to a subcommand."""
    f = click.option(
        "--grid-url",
        envvar="NIOS_GRID_URL",
        required=True,
        help="Grid Manager URL (e.g. https://gm.example.com). Falls back to NIOS_GRID_URL.",
    )(f)
    f = click.option(
        "--username",
        envvar="NIOS_USERNAME",
        required=True,
        help="NIOS admin username. Falls back to NIOS_USERNAME.",
    )(f)
    f = click.option(
        "--password",
        envvar="NIOS_PASSWORD",
        required=True,
        hide_input=True,
        help="NIOS admin password. Falls back to NIOS_PASSWORD.",
    )(f)
    f = click.option(
        "--wapi-ver",
        envvar="NIOS_WAPI_VERSION",
        default="2.14",
        show_default=True,
        help="NIOS WAPI version (default 2.14). Falls back to NIOS_WAPI_VERSION.",
    )(f)
    f = click.option(
        "--verify/--no-verify",
        default=True,
        show_default=True,
        help="Verify TLS certificates. Use --no-verify for lab grids with self-signed certs.",
    )(f)
    return f


@click.group()
def cli():
    """NIOS Fileop multi-step workflows - CSV import/export, support bundles, logs, certs."""


# ---------------------------------------------------------------------------
# CSV Export
# ---------------------------------------------------------------------------


@cli.command("csv-export")
@_shared_options
@click.option(
    "--object",
    "obj",
    required=True,
    help="WAPI object type to export (e.g. network, record:host, fixedaddress).",
)
@click.option(
    "--output", required=True, type=click.Path(), help="Output file path to save the exported CSV."
)
def csv_export_cmd(grid_url, username, password, wapi_ver, verify, obj, output):
    """Export NIOS objects as CSV and save to a local file.

    \b
    Full round-trip:
      1. POST /fileop?_function=csv_export  -> get token + download URL
      2. GET  <download URL>                -> download CSV content
      3. POST /fileop?_function=downloadcomplete  -> acknowledge completion
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            click.echo(f"Requesting CSV export for object type: {obj}")

            # Step 1: Initiate the export - returns token + url
            result = await client.misc.fileop.csv_export(_object=obj)
            if "token" not in result or "url" not in result:
                raise click.ClickException(
                    f"Unexpected csv_export response (missing token/url): {result}"
                )
            token = result["token"]
            url = result["url"]
            click.echo(f"Export initiated. Token: {token}")
            click.echo(f"Download URL: {url}")

            # Step 2: Download the CSV file using the underlying httpx client
            # (the session cookie from authentication is already present)
            resp = await client._http._client.get(url)
            resp.raise_for_status()
            with open(output, "wb") as f:
                f.write(resp.content)
            size = len(resp.content)
            click.echo(f"Downloaded {size:,} bytes -> {output}")

            # Step 3: Acknowledge completion so NIOS can clean up the temp file
            await client.misc.fileop.download_complete(token=token)
            click.echo("Download acknowledged. Export complete.")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# CSV Import
# ---------------------------------------------------------------------------


@cli.command("csv-import")
@_shared_options
@click.option(
    "--object",
    "obj",
    required=True,
    help="WAPI object type to import (e.g. network, record:host, fixedaddress).",
)
@click.option(
    "--input",
    "input_file",
    required=True,
    type=click.Path(exists=True),
    help="Path to the CSV file to import.",
)
@click.option(
    "--operation",
    type=click.Choice(["INSERT", "OVERRIDE", "MERGE", "DELETE", "CUSTOM"], case_sensitive=False),
    default="INSERT",
    show_default=True,
    help="Import operation mode.",
)
@click.option(
    "--on-error",
    type=click.Choice(["STOP", "SKIP", "CONTINUE"], case_sensitive=False),
    default="STOP",
    show_default=True,
    help="Error handling strategy.",
)
def csv_import_cmd(
    grid_url, username, password, wapi_ver, verify, obj, input_file, operation, on_error
):
    """Import objects from a local CSV file into NIOS.

    \b
    Full round-trip:
      1. POST /fileop?_function=uploadinit  -> get upload token + upload URL
      2. PUT  <upload URL> with CSV content -> upload the file
      3. POST /fileop?_function=csv_import  -> start the import job
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            click.echo(f"Preparing CSV import for object type: {obj}")
            click.echo(f"  Input file: {input_file}")
            click.echo(f"  Operation:  {operation.upper()}")

            # Step 1: Initiate the upload session
            init_result = await client.misc.fileop.upload_init()
            if "token" not in init_result or "url" not in init_result:
                raise click.ClickException(
                    f"Unexpected uploadinit response (missing token/url): {init_result}"
                )
            token = init_result["token"]
            upload_url = init_result["url"]
            click.echo(f"Upload session initiated. Token: {token}")
            click.echo(f"Upload URL: {upload_url}")

            # Step 2: Upload the CSV file via PUT using the underlying httpx client
            # (the session cookie from authentication is already present)
            with open(input_file, "rb") as f:
                csv_content = f.read()
            click.echo(f"Uploading {len(csv_content):,} bytes...")
            upload_resp = await client._http._client.put(
                upload_url,
                content=csv_content,
                headers={"Content-Type": "application/octet-stream"},
            )
            upload_resp.raise_for_status()
            click.echo("File uploaded successfully.")

            # Step 3: Kick off the import job
            import_result = await client.misc.fileop.csv_import(
                token=token,
                _object=obj,
                action="START",
                operation=operation.upper(),
                on_error=on_error.upper(),
            )
            import_id = import_result.get("csv_import_task_ref") or import_result.get("import_id")
            click.echo("Import job started.")
            if import_id:
                click.echo(f"  Task ref: {import_id}")
            click.echo(f"  Response: {import_result}")
            click.echo(
                "\nNote: Monitor the import task via the NIOS GUI or csvimporttask WAPI object."
            )

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Support Bundle
# ---------------------------------------------------------------------------


@cli.command("support-bundle")
@_shared_options
@click.option("--member", required=True, help="Grid member FQDN or IP to collect the bundle from.")
@click.option(
    "--output",
    required=True,
    type=click.Path(),
    help="Output file path for the support bundle archive.",
)
def support_bundle_cmd(grid_url, username, password, wapi_ver, verify, member, output):
    """Download a support bundle from a grid member.

    \b
    Full round-trip:
      1. POST /fileop?_function=get_support_bundle  -> token + url
      2. GET  <download URL>                         -> download bundle
      3. POST /fileop?_function=downloadcomplete     -> acknowledge
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            click.echo(f"Requesting support bundle from member: {member}")

            # Step 1: Request the support bundle
            result = await client.misc.fileop.call("get_support_bundle", member=member)
            if "token" not in result or "url" not in result:
                raise click.ClickException(
                    f"Unexpected get_support_bundle response (missing token/url): {result}"
                )
            token = result["token"]
            url = result["url"]
            click.echo(f"Bundle ready. Token: {token}")

            # Step 2: Download the bundle using the underlying httpx client
            resp = await client._http._client.get(url)
            resp.raise_for_status()
            with open(output, "wb") as f:
                f.write(resp.content)
            size = len(resp.content)
            click.echo(f"Downloaded {size:,} bytes -> {output}")

            # Step 3: Acknowledge completion
            await client.misc.fileop.download_complete(token=token)
            click.echo("Support bundle download complete.")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Global Search
# ---------------------------------------------------------------------------


@cli.command("search")
@_shared_options
@click.argument("query")
@click.option(
    "--max-results",
    default=100,
    show_default=True,
    type=int,
    help="Maximum number of search results to return.",
)
@click.option(
    "--objtype",
    default=None,
    help="Restrict results to a specific WAPI object type (e.g. record:host).",
)
def search_cmd(grid_url, username, password, wapi_ver, verify, query, max_results, objtype):
    """Search across all NIOS objects matching QUERY.

    \b
    QUERY - Search string matched against object attributes (e.g. "192.168.1", "host.example.com")
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            click.echo(f"Searching for: {query!r}")
            if objtype:
                click.echo(f"  (restricted to object type: {objtype})")

            kwargs = {
                "search_string": query,
                "_max_results": max_results,
            }
            if objtype:
                kwargs["objtype"] = objtype

            results = await client.misc.search.search(**kwargs)

            if not results:
                click.echo("No results found.")
                return

            click.echo(f"\n{'Type':<30} {'Ref'}")
            click.echo("-" * 90)
            for item in results:
                ref = item.get("_ref", "")
                obj_type = ref.split("/")[0] if "/" in ref else ref
                click.echo(f"{obj_type[:29]:<30} {ref}")

            click.echo(f"\nTotal: {len(results)} result(s)")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Log File Download
# ---------------------------------------------------------------------------


@cli.command("get-log")
@_shared_options
@click.option("--member", required=True, help="Grid member FQDN or IP.")
@click.option(
    "--log-type",
    type=click.Choice(
        [
            "SYSLOG",
            "AUDITLOG",
            "MSMGMTLOG",
            "DELTALOG",
            "OUTBOUND",
            "PTOPLOG",
            "DISCOVERY_CSV_ERRLOG",
        ],
        case_sensitive=False,
    ),
    default="SYSLOG",
    show_default=True,
    help="Type of log file to download.",
)
@click.option("--output", required=True, type=click.Path(), help="Output file path for the log.")
@click.option(
    "--node-type",
    type=click.Choice(["ACTIVE", "PASSIVE"], case_sensitive=False),
    default="ACTIVE",
    show_default=True,
    help="Node type for HA members.",
)
def get_log_cmd(
    grid_url, username, password, wapi_ver, verify, member, log_type, output, node_type
):
    """Download a log file from a grid member.

    \b
    Full round-trip:
      1. POST /fileop?_function=get_log_files  -> token + url
      2. GET  <download URL>                   -> download log
      3. POST /fileop?_function=downloadcomplete -> acknowledge
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            click.echo(f"Requesting {log_type} log from member: {member}")

            # Step 1: Request log file
            result = await client.misc.fileop.call(
                "get_log_files",
                member=member,
                log_type=log_type.upper(),
                node_type=node_type.upper(),
            )
            if "token" not in result or "url" not in result:
                raise click.ClickException(
                    f"Unexpected get_log_files response (missing token/url): {result}"
                )
            token = result["token"]
            url = result["url"]
            click.echo(f"Log ready. Token: {token}")

            # Step 2: Download the log file using the underlying httpx client
            resp = await client._http._client.get(url)
            resp.raise_for_status()
            with open(output, "wb") as f:
                f.write(resp.content)
            size = len(resp.content)
            click.echo(f"Downloaded {size:,} bytes -> {output}")

            # Step 3: Acknowledge completion
            await client.misc.fileop.download_complete(token=token)
            click.echo(f"{log_type} log download complete.")

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Certificate Download
# ---------------------------------------------------------------------------


@cli.command("get-cert")
@_shared_options
@click.option(
    "--cert-type",
    type=click.Choice(["HTTPS", "COMMS", "SAML"], case_sensitive=False),
    default="HTTPS",
    show_default=True,
    help="Certificate type to download.",
)
@click.option(
    "--member", default=None, help="Grid member FQDN or IP (omit for grid-level certificate)."
)
@click.option(
    "--output",
    required=True,
    type=click.Path(),
    help="Output file path for the certificate (PEM format).",
)
def get_cert_cmd(grid_url, username, password, wapi_ver, verify, cert_type, member, output):
    """Download a TLS certificate from NIOS.

    \b
    Full round-trip:
      1. POST /fileop?_function=downloadcertificate  -> token + url
      2. GET  <download URL>                          -> download certificate
      3. POST /fileop?_function=downloadcomplete      -> acknowledge
    """

    async def run():
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            scope = f"member {member}" if member else "grid"
            click.echo(f"Requesting {cert_type} certificate for {scope}")

            # Map CLI cert-type to WAPI certificate_usage values
            usage_map = {
                "HTTPS": "HTTP_CERT",
                "COMMS": "COMMS_CERT",
                "SAML": "SAML_CERT",
            }
            certificate_usage = usage_map[cert_type.upper()]

            # Step 1: Request the certificate download token
            kwargs = {"certificate_usage": certificate_usage}
            if member:
                kwargs["member"] = member
            result = await client.misc.fileop.downloadcertificate(**kwargs)
            if "token" not in result or "url" not in result:
                raise click.ClickException(
                    f"Unexpected downloadcertificate response (missing token/url): {result}"
                )
            token = result["token"]
            url = result["url"]
            click.echo(f"Certificate ready. Token: {token}")

            # Step 2: Download the certificate using the underlying httpx client
            resp = await client._http._client.get(url)
            resp.raise_for_status()
            with open(output, "wb") as f:
                f.write(resp.content)
            size = len(resp.content)
            click.echo(f"Downloaded {size:,} bytes -> {output}")

            # Step 3: Acknowledge completion
            await client.misc.fileop.download_complete(token=token)
            click.echo(f"{cert_type} certificate saved to: {output}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
