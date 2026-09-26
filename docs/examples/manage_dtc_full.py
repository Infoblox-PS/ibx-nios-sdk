# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Complete NIOS DTC (GSLB) lifecycle management - end-to-end workflow.

This script demonstrates a realistic GSLB configuration lifecycle:

  deploy   → Create monitors → servers → pool → LBDN from scratch
  teardown → Tear down an LBDN and all its dependent objects
  status   → Walk LBDN → pools → servers/monitors and print a tree view
  health   → Report availability status for all DTC objects
  migrate  → Add a new pool to an existing LBDN without disrupting traffic

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as defaults):
    NIOS_GRID_URL      - Grid URL, e.g. https://192.168.1.2
    NIOS_USERNAME      - WAPI username
    NIOS_PASSWORD      - WAPI password
    NIOS_WAPI_VERSION  - WAPI version (default: 2.14)

----------------------------------------------------------------------------
FULL WALKTHROUGH EXAMPLE
----------------------------------------------------------------------------

1. Set credentials:

    export NIOS_GRID_URL=https://192.168.1.2
    export NIOS_USERNAME=admin
    export NIOS_PASSWORD=infoblox
    export NIOS_WAPI_VERSION=2.14

2. Deploy a complete GSLB config for app.example.com:

    python manage_dtc_full.py deploy \\
        --lbdn-name "app.example.com" \\
        --patterns "app.example.com" \\
        --servers "app-east:10.0.0.1" "app-west:10.0.1.1" \\
        --monitor-type http \\
        --monitor-port 80 \\
        --lb-method ROUND_ROBIN \\
        --ttl 300

    Output (example):
        [OK] Created HTTP monitor:  dtc:monitor:http/ZG5z...:http-80-mon
        [OK] Created DTC server:    dtc:server/ZG5z...:app-east
        [OK] Created DTC server:    dtc:server/ZG5z...:app-west
        [OK] Created DTC pool:      dtc:pool/ZG5z...:app.example.com-pool
        [OK] Created DTC LBDN:      dtc:lbdn/ZG5z...:app.example.com

3. Inspect the deployed config:

    python manage_dtc_full.py status --lbdn-name "app.example.com"

    Output:
        LBDN: app.example.com  (ROUND_ROBIN, ttl=300)
          Pool: app.example.com-pool  (ratio=1)
            Monitor: http-80-mon  [HTTP]
            Server: app-east  (10.0.0.1, ratio=1)
            Server: app-west  (10.0.1.1, ratio=1)

4. Add a new pool (blue-green migration):

    python manage_dtc_full.py migrate \\
        --lbdn-ref dtc:lbdn/ZG5z... \\
        --new-pool-ref dtc:pool/ZG5z...-v2 \\
        --ratio 1

5. Check health across all DTC objects:

    python manage_dtc_full.py health

6. Tear down the entire config:

    python manage_dtc_full.py teardown --lbdn-name "app.example.com"
    # (prompts for confirmation; use --force to skip)

----------------------------------------------------------------------------
API NOTES
----------------------------------------------------------------------------

Pool servers list format (NIOS WAPI):
    {"server": "<dtc:server ref>", "ratio": <int>}

Pool monitors list format:
    "<dtc:monitor:* ref>"  - bare object reference string (monitor_type is auto-detected by WAPI)

LBDN pools list format:
    {"pool": "<dtc:pool ref>", "ratio": <int>}

Deletion dependency order (must respect):
    LBDN → Pool → Server → Monitor
    (removing in reverse prevents "object in use" WAPI errors)
"""

from __future__ import annotations

import asyncio
import logging

import click

from ibx_nios_sdk import NiosClient

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------


def _connect(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> NiosClient:
    """Construct a NiosClient from the shared connection options."""
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
    f = click.option(
        "--verbose",
        is_flag=True,
        default=False,
        help="Enable verbose debug logging.",
    )(f)
    return f


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _setup_logging(verbose: bool) -> None:
    """Configure logging level based on the --verbose flag."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
    )


async def _find_lbdn_by_name(client: NiosClient, lbdn_name: str) -> object:
    """Find an LBDN by display name. Returns the model or raises ClickException."""
    results = await client.dtc.lbdn.list(
        name=lbdn_name,
        return_fields_plus=["pools", "patterns", "ttl", "lb_method", "health"],
    ).all()
    if not results:
        raise click.ClickException(
            f"No LBDN found with name '{lbdn_name}'. "
            "Use 'deploy' to create one, or check the name."
        )
    return results[0]


async def _get_pool_detail(client: NiosClient, pool_ref: str) -> object:
    """Fetch a pool with its servers and monitors fields."""
    return await client.dtc.pool.get(
        pool_ref,
        return_fields_plus=[
            "servers",
            "monitors",
            "lb_preferred_method",
            "availability",
            "health",
            "name",
        ],
    )


async def _get_server_detail(client: NiosClient, server_ref: str) -> object:
    """Fetch a server with its host and health fields."""
    return await client.dtc.server.get(
        server_ref,
        return_fields_plus=["host", "health", "name"],
    )


async def _delete_ref_safe(client: NiosClient, ref: str, label: str) -> None:
    """Delete a WAPI object by ref; log and continue on errors."""
    try:
        if ref.startswith("dtc:lbdn/"):
            await client.dtc.lbdn.delete(ref)
        elif ref.startswith("dtc:pool/"):
            await client.dtc.pool.delete(ref)
        elif ref.startswith("dtc:server/"):
            await client.dtc.server.delete(ref)
        elif ref.startswith("dtc:monitor:http/"):
            await client.dtc.monitor_http.delete(ref)
        elif ref.startswith("dtc:monitor:tcp/"):
            await client.dtc.monitor_tcp.delete(ref)
        elif ref.startswith("dtc:monitor:icmp/"):
            await client.dtc.monitor_icmp.delete(ref)
        elif ref.startswith("dtc:monitor:sip/"):
            await client.dtc.monitor_sip.delete(ref)
        elif ref.startswith("dtc:monitor:snmp/"):
            await client.dtc.monitor_snmp.delete(ref)
        elif ref.startswith("dtc:monitor:pdp/"):
            await client.dtc.monitor_pdp.delete(ref)
        else:
            click.secho(f"  [WARN] Unknown ref type, skipping: {ref}", fg="yellow")
            return
        click.secho(f"  [OK] Deleted {label}: {ref}", fg="green")
    except Exception as exc:  # noqa: BLE001
        click.secho(f"  [ERR] Failed to delete {label} {ref}: {exc}", fg="red")


# ---------------------------------------------------------------------------
# Root CLI group
# ---------------------------------------------------------------------------


@click.group()
def cli() -> None:
    """Complete NIOS DTC / GSLB lifecycle management.

    \b
    deploy    Build a complete DTC config from scratch.
    teardown  Remove an LBDN and all its dependent objects.
    status    Print a tree view of a live LBDN configuration.
    health    Report availability status for all DTC objects.
    migrate   Add a new pool to an existing LBDN.
    """


# ===========================================================================
# deploy
# ===========================================================================


@cli.command("deploy")
@_shared_options
@click.option(
    "--lbdn-name",
    default="app.example.com",
    show_default=True,
    help="Display name for the LBDN (also used to name the pool).",
)
@click.option(
    "--patterns",
    multiple=True,
    default=["app.example.com"],
    show_default=True,
    help="DNS wildcard pattern(s) matched by the LBDN (repeatable).",
)
@click.option(
    "--servers",
    multiple=True,
    required=True,
    help="Servers in NAME:IP format, e.g. app-east:10.0.0.1 (repeatable).",
)
@click.option(
    "--monitor-type",
    default="http",
    show_default=True,
    type=click.Choice(["http", "tcp", "icmp"], case_sensitive=False),
    help="Type of health monitor to create.",
)
@click.option(
    "--monitor-port",
    default=80,
    show_default=True,
    type=int,
    help="Port for the HTTP or TCP monitor (ignored for ICMP).",
)
@click.option(
    "--lb-method",
    default="ROUND_ROBIN",
    show_default=True,
    type=click.Choice(
        ["ROUND_ROBIN", "RATIO", "GLOBAL_AVAILABILITY", "TOPOLOGY", "DYNAMIC_RATIO"],
        case_sensitive=False,
    ),
    help="LBDN-level load-balancing method.",
)
@click.option(
    "--ttl",
    default=300,
    show_default=True,
    type=int,
    help="DNS TTL in seconds for LBDN responses.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Print what would be created without making any API calls.",
)
def cmd_deploy(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    verbose: bool,
    lbdn_name: str,
    patterns: tuple[str, ...],
    servers: tuple[str, ...],
    monitor_type: str,
    monitor_port: int,
    lb_method: str,
    ttl: int,
    dry_run: bool,
) -> None:
    """Deploy a complete GSLB configuration from scratch.

    Creates (in order):

    \b
    1. A health monitor of the requested type
    2. One DTC server per --servers entry (NAME:IP format)
    3. A DTC pool referencing all servers with equal ratio
    4. A DTC LBDN binding the pool to the requested DNS pattern(s)

    All created refs are printed at the end for use in subsequent commands.
    Use --dry-run to preview what would be created without touching the grid.
    """
    _setup_logging(verbose)

    # Parse server specs
    parsed_servers: list[tuple[str, str]] = []
    for spec in servers:
        if ":" not in spec:
            raise click.UsageError(f"Server spec must be NAME:IP, got '{spec}'")
        srv_name, srv_ip = spec.split(":", 1)
        parsed_servers.append((srv_name.strip(), srv_ip.strip()))

    monitor_name = f"{lbdn_name.replace('.', '-')}-{monitor_type}-{monitor_port}-mon"
    pool_name = f"{lbdn_name}-pool"

    if dry_run:
        click.echo("[DRY RUN] The following objects would be created:")
        click.echo(f"  Monitor ({monitor_type}): name={monitor_name}, port={monitor_port}")
        for srv_name, srv_ip in parsed_servers:
            click.echo(f"  Server:              name={srv_name}, host={srv_ip}")
        click.echo(
            f"  Pool:                name={pool_name}, method={lb_method.upper()}, "
            f"servers={[s[0] for s in parsed_servers]}"
        )
        click.echo(
            f"  LBDN:                name={lbdn_name}, patterns={list(patterns)}, "
            f"ttl={ttl}, lb_method={lb_method.upper()}"
        )
        return

    async def run() -> None:
        created_refs: dict[str, str] = {}  # label -> ref

        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # ----------------------------------------------------------------
            # Step 1: Create monitor
            # ----------------------------------------------------------------
            click.echo(f"\n[1/4] Creating {monitor_type.upper()} monitor '{monitor_name}'...")
            logger.debug("monitor_name=%s port=%d", monitor_name, monitor_port)

            if monitor_type == "http":
                monitor = await client.dtc.monitor_http.create(
                    {
                        "name": monitor_name,
                        "port": monitor_port,
                        "timeout": 15,
                        "retry_up": 1,
                        "retry_down": 1,
                    },
                    return_fields_plus=["port"],
                )
            elif monitor_type == "tcp":
                monitor = await client.dtc.monitor_tcp.create(
                    {"name": monitor_name, "port": monitor_port},
                    return_fields_plus=["port"],
                )
            else:  # icmp
                monitor = await client.dtc.monitor_icmp.create({"name": monitor_name})

            monitor_ref = monitor.ref
            created_refs["Monitor"] = monitor_ref
            click.secho(
                f"  [OK] Created {monitor_type.upper()} monitor: {monitor_ref}", fg="green"
            )

            # ----------------------------------------------------------------
            # Step 2: Create servers
            # ----------------------------------------------------------------
            click.echo(f"\n[2/4] Creating {len(parsed_servers)} DTC server(s)...")
            server_refs: list[str] = []
            for srv_name, srv_ip in parsed_servers:
                logger.debug("Creating server name=%s host=%s", srv_name, srv_ip)
                server = await client.dtc.server.create(
                    {"name": srv_name, "host": srv_ip},
                    return_fields_plus=["host"],
                )
                srv_ref = server.ref
                server_refs.append(srv_ref)
                created_refs[f"Server:{srv_name}"] = srv_ref
                click.secho(f"  [OK] Created DTC server: {srv_ref}", fg="green")

            # ----------------------------------------------------------------
            # Step 3: Create pool
            # ----------------------------------------------------------------
            click.echo(f"\n[3/4] Creating DTC pool '{pool_name}'...")
            logger.debug("pool_name=%s servers=%d", pool_name, len(server_refs))

            pool = await client.dtc.pool.create(
                {
                    "name": pool_name,
                    "lb_preferred_method": lb_method.upper(),
                    "servers": [{"server": ref, "ratio": 1} for ref in server_refs],
                    "monitors": [monitor_ref],
                },
                return_fields_plus=["servers", "monitors", "lb_preferred_method"],
            )
            pool_ref = pool.ref
            created_refs["Pool"] = pool_ref
            click.secho(f"  [OK] Created DTC pool: {pool_ref}", fg="green")

            # ----------------------------------------------------------------
            # Step 4: Create LBDN
            # ----------------------------------------------------------------
            click.echo(f"\n[4/4] Creating DTC LBDN '{lbdn_name}'...")
            logger.debug("lbdn_name=%s patterns=%s", lbdn_name, patterns)

            lbdn = await client.dtc.lbdn.create(
                {
                    "name": lbdn_name,
                    "lb_method": lb_method.upper(),
                    "pools": [{"pool": pool_ref, "ratio": 1}],
                    "patterns": list(patterns),
                    "ttl": ttl,
                    "use_ttl": True,
                },
                return_fields_plus=["pools", "patterns", "ttl", "lb_method"],
            )
            lbdn_ref = lbdn.ref
            created_refs["LBDN"] = lbdn_ref
            click.secho(f"  [OK] Created DTC LBDN: {lbdn_ref}", fg="green")

        # ----------------------------------------------------------------
        # Summary
        # ----------------------------------------------------------------
        click.echo("\n" + "=" * 60)
        click.echo("DEPLOY SUMMARY")
        click.echo("=" * 60)
        for label, ref in created_refs.items():
            click.echo(f"  {label:<20} {ref}")
        click.echo()
        click.echo("Tip: save these refs for teardown, migrate, and status commands.")

    asyncio.run(run())


# ===========================================================================
# teardown
# ===========================================================================


@cli.command("teardown")
@_shared_options
@click.option(
    "--lbdn-name",
    required=True,
    help="Display name of the LBDN to tear down.",
)
@click.option(
    "--force/--no-force",
    default=False,
    show_default=True,
    help="Skip all confirmation prompts.",
)
def cmd_teardown(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    verbose: bool,
    lbdn_name: str,
    force: bool,
) -> None:
    """Tear down a complete DTC GSLB config by LBDN name.

    Walks the LBDN to collect all dependent pool, server, and monitor refs,
    then deletes them in the correct dependency order:

    \b
    1. LBDN  (must go first - it references the pools)
    2. Pools (each references servers and monitors)
    3. Servers
    4. Monitors

    Use --force to suppress all confirmation prompts.
    """
    _setup_logging(verbose)

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # ----------------------------------------------------------------
            # Discovery phase - collect all refs
            # ----------------------------------------------------------------
            click.echo(f"\nLooking up LBDN '{lbdn_name}'...")
            lbdn = await _find_lbdn_by_name(client, lbdn_name)

            lbdn_ref = lbdn.ref
            pool_entries: list[dict] = lbdn.pools or []
            pool_refs = [e.get("pool") for e in pool_entries if e.get("pool")]

            server_refs: list[str] = []
            monitor_refs: list[str] = []

            for pool_ref in pool_refs:
                logger.debug("Fetching pool detail: %s", pool_ref)
                pool = await _get_pool_detail(client, pool_ref)
                for srv_entry in pool.servers or []:
                    ref = srv_entry.get("server")
                    if ref and ref not in server_refs:
                        server_refs.append(ref)
                for mon_entry in pool.monitors or []:
                    # monitors list contains bare ref strings
                    ref = mon_entry if isinstance(mon_entry, str) else mon_entry.get("monitor")
                    if ref and ref not in monitor_refs:
                        monitor_refs.append(ref)

            # ----------------------------------------------------------------
            # Confirmation
            # ----------------------------------------------------------------
            click.echo()
            click.echo("Objects to be deleted:")
            click.echo(f"  LBDN:     {lbdn_ref}")
            for r in pool_refs:
                click.echo(f"  Pool:     {r}")
            for r in server_refs:
                click.echo(f"  Server:   {r}")
            for r in monitor_refs:
                click.echo(f"  Monitor:  {r}")
            click.echo()

            total = 1 + len(pool_refs) + len(server_refs) + len(monitor_refs)
            if not force:
                click.confirm(f"Permanently delete {total} DTC object(s)?", abort=True)

            # ----------------------------------------------------------------
            # Deletion - in dependency order
            # ----------------------------------------------------------------
            click.echo("\nDeleting objects...")

            # 1. LBDN first
            await _delete_ref_safe(client, lbdn_ref, "LBDN")

            # 2. Pools
            for ref in pool_refs:
                await _delete_ref_safe(client, ref, "Pool")

            # 3. Servers
            for ref in server_refs:
                await _delete_ref_safe(client, ref, "Server")

            # 4. Monitors
            for ref in monitor_refs:
                await _delete_ref_safe(client, ref, "Monitor")

        # Summary
        click.echo()
        click.echo("=" * 60)
        click.echo("TEARDOWN COMPLETE")
        click.echo("=" * 60)
        click.echo("  LBDN deleted:      1")
        click.echo(f"  Pools deleted:     {len(pool_refs)}")
        click.echo(f"  Servers deleted:   {len(server_refs)}")
        click.echo(f"  Monitors deleted:  {len(monitor_refs)}")

    asyncio.run(run())


# ===========================================================================
# status
# ===========================================================================


@cli.command("status")
@_shared_options
@click.option(
    "--lbdn-name",
    required=True,
    help="Display name of the LBDN to inspect.",
)
def cmd_status(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    verbose: bool,
    lbdn_name: str,
) -> None:
    """Print a tree view of a live LBDN configuration.

    Walks the LBDN → pools → servers/monitors hierarchy and renders it as
    an indented ASCII tree, including any available health status.

    Example output:

    \b
    LBDN: app.example.com  (ROUND_ROBIN, ttl=300)
      Pool: app.example.com-pool  (ratio=1)
        Monitor: http-80-mon  [HTTP]
        Server: app-east  (10.0.0.1, ratio=1)
        Server: app-west  (10.0.1.1, ratio=1)
    """
    _setup_logging(verbose)

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            lbdn = await _find_lbdn_by_name(client, lbdn_name)

            # LBDN header
            health_str = ""
            if lbdn.health:
                health_str = f"  [{lbdn.health.get('flag', '?')}]"
            click.echo(
                f"LBDN: {lbdn.name}  "
                f"({lbdn.lb_method or 'N/A'}, ttl={lbdn.ttl or 'N/A'})"
                f"{health_str}"
            )

            pool_entries: list[dict] = lbdn.pools or []
            if not pool_entries:
                click.echo("  (no pools attached)")
                return

            for pool_entry in pool_entries:
                pool_ref = pool_entry.get("pool")
                pool_ratio = pool_entry.get("ratio", 1)
                if not pool_ref:
                    continue

                pool = await _get_pool_detail(client, pool_ref)
                pool_health_str = ""
                if pool.health:
                    pool_health_str = f"  [{pool.health.get('flag', '?')}]"

                click.echo(
                    f"  Pool: {pool.name or pool_ref}  "
                    f"(ratio={pool_ratio}, method={pool.lb_preferred_method or 'N/A'})"
                    f"{pool_health_str}"
                )

                # Monitors - WAPI returns bare ref strings
                for mon_entry in pool.monitors or []:
                    mon_ref = (
                        mon_entry if isinstance(mon_entry, str) else mon_entry.get("monitor", "")
                    )
                    # Derive a readable type hint from the ref prefix
                    if "monitor:http" in mon_ref:
                        mon_type = "HTTP"
                    elif "monitor:tcp" in mon_ref:
                        mon_type = "TCP"
                    elif "monitor:icmp" in mon_ref:
                        mon_type = "ICMP"
                    else:
                        mon_type = mon_ref.split(":")[2] if mon_ref.count(":") >= 2 else "?"
                    # Extract a readable name from the ref (last path segment)
                    mon_name_hint = mon_ref.split(":")[-1] if mon_ref else mon_ref
                    click.echo(f"    Monitor: {mon_name_hint}  [{mon_type}]")

                # Servers
                for srv_entry in pool.servers or []:
                    srv_ref = srv_entry.get("server", "")
                    srv_ratio = srv_entry.get("ratio", 1)
                    if not srv_ref:
                        continue

                    server = await _get_server_detail(client, srv_ref)
                    srv_health_str = ""
                    if server.health:
                        srv_health_str = f"  [{server.health.get('flag', '?')}]"

                    click.echo(
                        f"    Server: {server.name or srv_ref}  "
                        f"(host={server.host or 'N/A'}, ratio={srv_ratio})"
                        f"{srv_health_str}"
                    )

    asyncio.run(run())


# ===========================================================================
# health
# ===========================================================================


@cli.command("health")
@_shared_options
def cmd_health(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    verbose: bool,
) -> None:
    """Report availability status for all DTC objects.

    Queries the dtc:object aggregate view (which carries the health status
    flag for every DTC resource) and prints a tabular summary.  The
    ``status`` field reflects NIOS availability colour codes:

    \b
    GREEN  - All monitors report the object as up
    YELLOW - Some monitors report the object as degraded
    RED    - Object is down / unreachable
    BLUE   - No monitors assigned; status unknown
    """
    _setup_logging(verbose)

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            objects = await client.dtc.object.list(
                return_fields_plus=["status", "display_type", "object", "comment"],
            ).all()

            if not objects:
                click.echo("No DTC objects found (grid may have no DTC configuration).")
                return

            click.echo(f"{'Name':<30} {'Type':<18} {'Status':<10} {'Comment'}")
            click.echo("-" * 80)
            for obj in objects:
                status = obj.status or "UNKNOWN"
                color: str
                if status == "GREEN":
                    color = "green"
                elif status in ("YELLOW", "BLUE"):
                    color = "yellow"
                elif status == "RED":
                    color = "red"
                else:
                    color = "white"

                line = (
                    f"{obj.name or '':<30} "
                    f"{obj.display_type or '':<18} "
                    f"{status:<10} "
                    f"{obj.comment or ''}"
                )
                click.secho(line, fg=color)

            click.echo(f"\nTotal: {len(objects)} DTC object(s) reported")

    asyncio.run(run())


# ===========================================================================
# migrate
# ===========================================================================


@cli.command("migrate")
@_shared_options
@click.option(
    "--lbdn-ref",
    required=True,
    help="WAPI ref of the LBDN to update, e.g. dtc:lbdn/ZG5z...",
)
@click.option(
    "--new-pool-ref",
    required=True,
    help="WAPI ref of the new pool to add, e.g. dtc:pool/ZG5z...",
)
@click.option(
    "--ratio",
    default=1,
    show_default=True,
    type=int,
    help="Load-balancing weight for the new pool.",
)
def cmd_migrate(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    verbose: bool,
    lbdn_ref: str,
    new_pool_ref: str,
    ratio: int,
) -> None:
    """Add a new pool to an existing LBDN without disrupting traffic.

    Fetches the current LBDN pools list, appends the new pool entry, and
    PUTs the updated list back.  The operation is atomic from the NIOS
    perspective - existing pools continue to serve traffic during the update.

    Typical blue-green / canary migration pattern:

    \b
    1. Build and validate new pool with new servers.
    2. Run 'migrate' to add new pool at low ratio (e.g. --ratio 1).
    3. Monitor health via 'health' command.
    4. Remove old pool manually once traffic drains.
    """
    _setup_logging(verbose)

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # Fetch current LBDN
            lbdn = await client.dtc.lbdn.get(
                lbdn_ref,
                return_fields_plus=["pools", "name"],
            )

            current_pools: list[dict] = list(lbdn.pools or [])
            existing_pool_refs = {entry.get("pool") for entry in current_pools}

            if new_pool_ref in existing_pool_refs:
                click.echo(f"  Pool '{new_pool_ref}' is already in LBDN '{lbdn.name}'. No change.")
                return

            current_pools.append({"pool": new_pool_ref, "ratio": ratio})

            updated = await client.dtc.lbdn.update(
                lbdn_ref,
                {"pools": current_pools},
                return_fields_plus=["pools", "name"],
            )
            click.secho("  [OK] Pool added to LBDN", fg="green")
            click.echo(f"  LBDN: {updated.name}  ({lbdn_ref})")
            click.echo(f"  Total pools now: {len(updated.pools or [])}")
            for entry in updated.pools or []:
                click.echo(f"    pool={entry.get('pool')}  ratio={entry.get('ratio', 1)}")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
