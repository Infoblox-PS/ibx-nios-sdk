# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Manage NIOS DTC monitors, LBDNs, and topologies.

Provides subcommand groups for:
- ``monitors``  - create/list/delete HTTP, TCP, and ICMP health monitors
- ``lbdn``      - manage Load-Balanced Domain Name objects (dtc:lbdn)
- ``topology``  - manage topology objects and their rules (dtc:topology)

NIOS DTC health monitors use WAPI types:
    dtc:monitor:http   dtc:monitor:tcp   dtc:monitor:icmp
    dtc:monitor:sip    dtc:monitor:snmp  dtc:monitor:pdp

When attaching a monitor to a pool, the caller must supply the ref *and* a
``monitor_type`` string (e.g. "HTTP").  The manage_dtc_pools.py helper
infers ``monitor_type`` from the ref prefix.

Prerequisites:
    pip install ibx-nios-sdk click

Environment variables (used as defaults):
    NIOS_GRID_URL      - Grid URL, e.g. https://192.168.1.2
    NIOS_USERNAME      - WAPI username
    NIOS_PASSWORD      - WAPI password
    NIOS_WAPI_VERSION  - WAPI version (default: 2.14)

Example usage:

    # List HTTP monitors
    python manage_dtc.py monitors list-http

    # Create an HTTP monitor
    python manage_dtc.py monitors create-http --name http-80 --port 80

    # Create a TCP monitor
    python manage_dtc.py monitors create-tcp --name tcp-443 --port 443

    # Create an ICMP monitor
    python manage_dtc.py monitors create-icmp --name icmp-ping

    # Delete a monitor by ref
    python manage_dtc.py monitors delete-monitor dtc:monitor:http/ZG5z...

    # List LBDNs
    python manage_dtc.py lbdn list

    # Create an LBDN
    python manage_dtc.py lbdn create --name app.example.com \\
        --pools dtc:pool/ZG5z... --patterns "*.app.example.com"

    # List topologies
    python manage_dtc.py topology list

    # Create a topology
    python manage_dtc.py topology create --name geo-topology

    # Add a rule to a topology (written as an inline member of topology.rules)
    python manage_dtc.py topology add-rule dtc:topology/ZG5z... \\
        --dest-type POOL --dest-ref dtc:pool/ZG5z... \\
        --source-type SUBNET --source-value 10.0.0.0/8
"""

from __future__ import annotations

import asyncio

import click

from ibx_nios_sdk import NiosClient

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
    return f


# ---------------------------------------------------------------------------
# Root CLI group
# ---------------------------------------------------------------------------


@click.group()
def cli() -> None:
    """Manage NIOS DTC monitors, LBDNs, and topology objects.

    Use the sub-groups to work with specific resource categories:

    \b
    monitors   - HTTP / TCP / ICMP health monitor CRUD
    lbdn       - Load-Balanced Domain Name CRUD
    topology   - Topology and topology-rule management
    """


# ===========================================================================
# monitors sub-group
# ===========================================================================


@cli.group("monitors")
def monitors_group() -> None:
    """Manage DTC health monitors (HTTP, TCP, ICMP)."""


@monitors_group.command("list-http")
@_shared_options
def monitors_list_http(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> None:
    """List all DTC HTTP health monitors."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            items = await client.dtc.monitor_http.list().all()
            if not items:
                click.echo("No HTTP monitors found.")
                return
            click.echo(f"{'Name':<28} {'Port':<8} {'Secure':<8} {'Comment'}")
            click.echo("-" * 70)
            for m in items:
                click.echo(
                    f"{m.name or '':<28} "
                    f"{str(m.port or ''):<8} "
                    f"{str(m.secure or False):<8} "
                    f"{m.comment or ''}"
                )
            click.echo(f"\nTotal: {len(items)} HTTP monitor(s)")

    asyncio.run(run())


@monitors_group.command("list-tcp")
@_shared_options
def monitors_list_tcp(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> None:
    """List all DTC TCP health monitors."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            items = await client.dtc.monitor_tcp.list().all()
            if not items:
                click.echo("No TCP monitors found.")
                return
            click.echo(f"{'Name':<28} {'Port':<8} {'Comment'}")
            click.echo("-" * 55)
            for m in items:
                click.echo(f"{m.name or '':<28} {str(m.port or ''):<8} {m.comment or ''}")
            click.echo(f"\nTotal: {len(items)} TCP monitor(s)")

    asyncio.run(run())


@monitors_group.command("list-icmp")
@_shared_options
def monitors_list_icmp(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> None:
    """List all DTC ICMP health monitors."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            items = await client.dtc.monitor_icmp.list().all()
            if not items:
                click.echo("No ICMP monitors found.")
                return
            click.echo(f"{'Name':<28} {'Interval':<10} {'Timeout':<10} {'Comment'}")
            click.echo("-" * 65)
            for m in items:
                click.echo(
                    f"{m.name or '':<28} "
                    f"{str(m.interval or ''):<10} "
                    f"{str(m.timeout or ''):<10} "
                    f"{m.comment or ''}"
                )
            click.echo(f"\nTotal: {len(items)} ICMP monitor(s)")

    asyncio.run(run())


@monitors_group.command("create-http")
@_shared_options
@click.option("--name", required=True, help="Display name for the HTTP monitor.")
@click.option("--port", required=True, type=int, help="TCP port to probe (e.g. 80 or 443).")
@click.option(
    "--timeout",
    default=15,
    show_default=True,
    type=int,
    help="Probe timeout in seconds.",
)
@click.option(
    "--retry-up",
    default=1,
    show_default=True,
    type=int,
    help="Consecutive successes before marking a server UP.",
)
@click.option(
    "--retry-down",
    default=1,
    show_default=True,
    type=int,
    help="Consecutive failures before marking a server DOWN.",
)
@click.option("--comment", default=None, help="Optional comment.")
def monitors_create_http(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    port: int,
    timeout: int,
    retry_up: int,
    retry_down: int,
    comment: str | None,
) -> None:
    """Create a new DTC HTTP health monitor."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {
                "name": name,
                "port": port,
                "timeout": timeout,
                "retry_up": retry_up,
                "retry_down": retry_down,
            }
            if comment:
                body["comment"] = comment

            monitor = await client.dtc.monitor_http.create(
                body, return_fields_plus=["port", "timeout", "retry_up", "retry_down"]
            )
            click.secho("  [OK] HTTP monitor created", fg="green")
            click.echo(f"  ref:         {monitor.ref}")
            click.echo(f"  name:        {monitor.name}")
            click.echo(f"  port:        {monitor.port}")
            click.echo(f"  timeout:     {monitor.timeout}s")
            click.echo(f"  retry_up:    {monitor.retry_up}")
            click.echo(f"  retry_down:  {monitor.retry_down}")

    asyncio.run(run())


@monitors_group.command("create-tcp")
@_shared_options
@click.option("--name", required=True, help="Display name for the TCP monitor.")
@click.option("--port", required=True, type=int, help="TCP port to probe.")
@click.option("--comment", default=None, help="Optional comment.")
def monitors_create_tcp(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    port: int,
    comment: str | None,
) -> None:
    """Create a new DTC TCP health monitor."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {"name": name, "port": port}
            if comment:
                body["comment"] = comment

            monitor = await client.dtc.monitor_tcp.create(body, return_fields_plus=["port"])
            click.secho("  [OK] TCP monitor created", fg="green")
            click.echo(f"  ref:   {monitor.ref}")
            click.echo(f"  name:  {monitor.name}")
            click.echo(f"  port:  {monitor.port}")

    asyncio.run(run())


@monitors_group.command("create-icmp")
@_shared_options
@click.option("--name", required=True, help="Display name for the ICMP monitor.")
@click.option("--comment", default=None, help="Optional comment.")
def monitors_create_icmp(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    comment: str | None,
) -> None:
    """Create a new DTC ICMP (ping) health monitor."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {"name": name}
            if comment:
                body["comment"] = comment

            monitor = await client.dtc.monitor_icmp.create(body)
            click.secho("  [OK] ICMP monitor created", fg="green")
            click.echo(f"  ref:   {monitor.ref}")
            click.echo(f"  name:  {monitor.name}")

    asyncio.run(run())


@monitors_group.command("delete-monitor")
@_shared_options
@click.argument("ref")
def monitors_delete_monitor(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
) -> None:
    """Delete a DTC monitor by WAPI reference (REF).

    REF can be any monitor type ref:
        dtc:monitor:http/ZG5z...
        dtc:monitor:tcp/ZG5z...
        dtc:monitor:icmp/ZG5z...

    The monitor type is inferred from the ref prefix.
    """

    async def run() -> None:
        click.confirm(f"Delete DTC monitor '{ref}'?", abort=True)
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            # Dispatch to the correct typed resource based on the ref prefix
            if ref.startswith("dtc:monitor:http/"):
                deleted = await client.dtc.monitor_http.delete(ref)
            elif ref.startswith("dtc:monitor:tcp/"):
                deleted = await client.dtc.monitor_tcp.delete(ref)
            elif ref.startswith("dtc:monitor:icmp/"):
                deleted = await client.dtc.monitor_icmp.delete(ref)
            elif ref.startswith("dtc:monitor:sip/"):
                deleted = await client.dtc.monitor_sip.delete(ref)
            elif ref.startswith("dtc:monitor:snmp/"):
                deleted = await client.dtc.monitor_snmp.delete(ref)
            elif ref.startswith("dtc:monitor:pdp/"):
                deleted = await client.dtc.monitor_pdp.delete(ref)
            else:
                raise click.ClickException(f"Cannot determine monitor type from ref: {ref}")
            click.secho(f"  [OK] Deleted: {deleted}", fg="green")

    asyncio.run(run())


# ===========================================================================
# lbdn sub-group
# ===========================================================================


@cli.group("lbdn")
def lbdn_group() -> None:
    """Manage DTC Load-Balanced Domain Name objects (dtc:lbdn).

    An LBDN maps DNS name patterns to DTC pools and defines the top-level
    load-balancing method. It is the entry point for GSLB resolution.

    The ``pools`` field is a list of dicts:
        [{"pool": "<dtc:pool ref>", "ratio": 1}, ...]
    """


@lbdn_group.command("list")
@_shared_options
def lbdn_list(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> None:
    """List all DTC LBDN objects."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            items = await client.dtc.lbdn.list().all()
            if not items:
                click.echo("No LBDNs found.")
                return
            click.echo(f"{'Name':<30} {'LB Method':<18} {'Pools':<7} {'Comment'}")
            click.echo("-" * 75)
            for lb in items:
                pool_count = len(lb.pools or [])
                click.echo(
                    f"{lb.name or '':<30} "
                    f"{lb.lb_method or '':<18} "
                    f"{pool_count:<7} "
                    f"{lb.comment or ''}"
                )
            click.echo(f"\nTotal: {len(items)} LBDN(s)")

    asyncio.run(run())


@lbdn_group.command("get")
@_shared_options
@click.argument("ref")
def lbdn_get(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
) -> None:
    """Get full details of an LBDN by WAPI reference (REF)."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            lb = await client.dtc.lbdn.get(
                ref,
                return_fields_plus=[
                    "pools",
                    "patterns",
                    "ttl",
                    "use_ttl",
                    "disable",
                    "topology",
                    "types",
                    "health",
                ],
            )
            click.echo(f"  ref:        {lb.ref}")
            click.echo(f"  name:       {lb.name}")
            click.echo(f"  lb_method:  {lb.lb_method}")
            click.echo(f"  ttl:        {lb.ttl}")
            click.echo(f"  disable:    {lb.disable}")
            click.echo(f"  comment:    {lb.comment}")
            if lb.patterns:
                click.echo(f"  patterns:   {', '.join(lb.patterns)}")
            if lb.pools:
                click.echo(f"  pools ({len(lb.pools)}):")
                for entry in lb.pools:
                    click.echo(f"    pool={entry.get('pool')}  ratio={entry.get('ratio', 1)}")
            if lb.health:
                click.echo(f"  health:     {lb.health}")

    asyncio.run(run())


@lbdn_group.command("create")
@_shared_options
@click.option("--name", required=True, help="Display name for the LBDN.")
@click.option(
    "--pools",
    multiple=True,
    required=True,
    help="WAPI ref(s) of pools to attach (repeatable).",
)
@click.option(
    "--patterns",
    multiple=True,
    help="DNS wildcard pattern(s) matched by this LBDN (repeatable).",
)
@click.option(
    "--lb-method",
    default="ROUND_ROBIN",
    show_default=True,
    type=click.Choice(
        ["ROUND_ROBIN", "RATIO", "GLOBAL_AVAILABILITY", "TOPOLOGY", "DYNAMIC_RATIO"],
        case_sensitive=False,
    ),
    help="Top-level load-balancing method.",
)
@click.option(
    "--ttl",
    default=300,
    show_default=True,
    type=int,
    help="DNS TTL in seconds for responses from this LBDN.",
)
@click.option("--comment", default=None, help="Optional comment.")
def lbdn_create(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    pools: tuple[str, ...],
    patterns: tuple[str, ...],
    lb_method: str,
    ttl: int,
    comment: str | None,
) -> None:
    """Create a new DTC LBDN object.

    Each value passed to ``--pools`` becomes a pool member with ratio=1.
    """

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {
                "name": name,
                "lb_method": lb_method.upper(),
                "pools": [{"pool": p, "ratio": 1} for p in pools],
                "ttl": ttl,
                "use_ttl": True,
            }
            if patterns:
                body["patterns"] = list(patterns)
            if comment:
                body["comment"] = comment

            lb = await client.dtc.lbdn.create(
                body,
                return_fields_plus=["pools", "patterns", "ttl", "lb_method"],
            )
            click.secho("  [OK] LBDN created", fg="green")
            click.echo(f"  ref:        {lb.ref}")
            click.echo(f"  name:       {lb.name}")
            click.echo(f"  lb_method:  {lb.lb_method}")
            click.echo(f"  ttl:        {lb.ttl}")
            click.echo(f"  pools:      {len(lb.pools or [])} attached")
            click.echo(f"  patterns:   {lb.patterns}")

    asyncio.run(run())


@lbdn_group.command("delete")
@_shared_options
@click.argument("ref")
def lbdn_delete(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
) -> None:
    """Delete an LBDN by WAPI reference (REF).

    You will be prompted to confirm before deletion.
    """

    async def run() -> None:
        click.confirm(f"Delete LBDN '{ref}'?", abort=True)
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            deleted = await client.dtc.lbdn.delete(ref)
            click.secho(f"  [OK] Deleted: {deleted}", fg="green")

    asyncio.run(run())


# ===========================================================================
# topology sub-group
# ===========================================================================


@cli.group("topology")
def topology_group() -> None:
    """Manage DTC topology objects and rules (dtc:topology, dtc:topology:rule).

    Topologies define geographic or network-based routing rules. Each rule
    maps a source (e.g. remote IP / subnet) to a destination (pool or server).
    """


@topology_group.command("list")
@_shared_options
def topology_list(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
) -> None:
    """List all DTC topology objects."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            items = await client.dtc.topology.list(return_fields_plus=["rules"]).all()
            if not items:
                click.echo("No topologies found.")
                return
            click.echo(f"{'Name':<30} {'Rules':<8} {'Comment'}")
            click.echo("-" * 60)
            for t in items:
                rule_count = len(t.rules or [])
                click.echo(f"{t.name or '':<30} {rule_count:<8} {t.comment or ''}")
            click.echo(f"\nTotal: {len(items)} topology/topologies")

    asyncio.run(run())


@topology_group.command("create")
@_shared_options
@click.option("--name", required=True, help="Display name for the topology.")
@click.option("--comment", default=None, help="Optional comment.")
def topology_create(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    name: str,
    comment: str | None,
) -> None:
    """Create a new DTC topology object."""

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            body: dict = {"name": name}
            if comment:
                body["comment"] = comment

            topo = await client.dtc.topology.create(body)
            click.secho("  [OK] Topology created", fg="green")
            click.echo(f"  ref:   {topo.ref}")
            click.echo(f"  name:  {topo.name}")

    asyncio.run(run())


@topology_group.command("add-rule")
@_shared_options
@click.argument("topology_ref")
@click.option(
    "--dest-type",
    required=True,
    type=click.Choice(["POOL", "SERVER"], case_sensitive=False),
    help="Type of the rule destination.",
)
@click.option(
    "--dest-ref",
    required=True,
    help="WAPI ref of the destination pool or server.",
)
@click.option(
    "--priority",
    default=1,
    show_default=True,
    type=int,
    help="Destination priority within the rule.",
)
@click.option(
    "--source-type",
    default=None,
    type=click.Choice(
        ["SUBNET", "CONTINENT", "COUNTRY", "SUBDIVISION", "CITY", "EA0", "EA1", "EA2", "EA3"],
        case_sensitive=False,
    ),
    help="Source criterion type. Omit for the topology's default rule.",
)
@click.option(
    "--source-op",
    default="IS",
    show_default=True,
    type=click.Choice(["IS", "IS_NOT"], case_sensitive=False),
    help="Source operator.",
)
@click.option(
    "--source-value",
    default=None,
    help="Source criterion value, e.g. a CIDR block '10.0.0.0/8' or 'DE'.",
)
@click.option(
    "--return-type",
    default="REGULAR",
    show_default=True,
    type=click.Choice(["REGULAR", "NOERR", "NXDOMAIN"], case_sensitive=False),
    help="What the rule returns. Only REGULAR uses the destination.",
)
def topology_add_rule(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    topology_ref: str,
    dest_type: str,
    dest_ref: str,
    priority: int,
    source_type: str | None,
    source_op: str,
    source_value: str | None,
    return_type: str,
) -> None:
    """Add a routing rule to a topology (TOPOLOGY_REF).

    TOPOLOGY_REF - WAPI ref of the target dtc:topology, e.g. dtc:topology/ZG5z...

    WAPI restricts create and delete on dtc:topology:rule, so rules are not
    created directly - they are written as inline members of the topology's
    ``rules`` list. This command reads the topology's existing rules, rebuilds
    them as request bodies, appends the new one, and PUTs the whole list.
    """

    # Fields to read back from each existing rule so it can be re-sent.
    RULE_FIELDS = ["dest_type", "return_type", "sources", "destination"]

    def rule_as_body(rule: dict) -> dict:
        """Turn a rule read from the grid back into a writable rule body."""
        body = {key: value for key, value in rule.items() if key in RULE_FIELDS}
        for destination in body.get("destination") or []:
            link = destination.get("destination_link")
            # NIOS returns destination_link as an inline object but only
            # accepts a _ref string on write.
            if isinstance(link, dict):
                destination["destination_link"] = link.get("_ref")
        return body

    async def run() -> None:
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            new_rule: dict = {
                "dest_type": dest_type.upper(),
                "return_type": return_type.upper(),
                "destination": [{"destination_link": dest_ref, "priority": priority}],
            }
            if source_type and source_value:
                new_rule["sources"] = [
                    {
                        "source_type": source_type.upper(),
                        "source_op": source_op.upper(),
                        "source_value": source_value,
                    }
                ]

            # Existing rules come back as inline stubs carrying only _ref/uuid,
            # so each one is fetched in full before being re-sent.
            topo = await client.dtc.topology.get(topology_ref, return_fields_plus=["rules"])
            bodies: list[dict] = []
            for stub in topo.rules or []:
                ref = stub.get("_ref") if isinstance(stub, dict) else stub
                existing = await client.dtc.topology_rule.get(ref, return_fields=RULE_FIELDS)
                bodies.append(rule_as_body(existing.model_dump(by_alias=True, exclude_none=True)))
            bodies.append(new_rule)

            updated = await client.dtc.topology.update(
                topology_ref, {"rules": bodies}, return_fields_plus=["rules"]
            )
            click.secho("  [OK] Topology rule added", fg="green")
            click.echo(f"  topology:  {topology_ref}")
            click.echo(f"  rules now: {len(updated.rules or [])}")

    asyncio.run(run())


@topology_group.command("delete")
@_shared_options
@click.argument("ref")
def topology_delete(
    grid_url: str,
    username: str,
    password: str,
    wapi_ver: str,
    verify: bool,
    ref: str,
) -> None:
    """Delete a DTC topology by WAPI reference (REF).

    REF is the WAPI object reference, e.g. dtc:topology/ZG5z...
    You will be prompted to confirm before deletion.
    """

    async def run() -> None:
        click.confirm(f"Delete DTC topology '{ref}'?", abort=True)
        async with _connect(grid_url, username, password, wapi_ver, verify) as client:
            deleted = await client.dtc.topology.delete(ref)
            click.secho(f"  [OK] Deleted: {deleted}", fg="green")

    asyncio.run(run())


if __name__ == "__main__":
    cli()
