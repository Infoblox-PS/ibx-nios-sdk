# Common Patterns

This page covers the patterns that apply across all 17 WAPI domains.

---

## Pagination

NIOS WAPI paginates large result sets. The SDK abstracts this away with `AsyncPageIterator`.

### Iterate page by page (memory-efficient)

```python
async with NiosClient() as client:
    async for zone in client.dns.zone_auth.list(view="default"):
        print(zone.fqdn)
```

### Collect all results at once

```python
async with NiosClient() as client:
    zones = await client.dns.zone_auth.list(view="default").all()
    print(f"{len(zones)} zones")
```

### Fetch a single page manually

```python
async with NiosClient() as client:
    rows, next_page_id = await client.dns.zone_auth.list_page(
        max_results=100,
        view="default",
    )
    # rows: list[ZoneAuth], next_page_id: str | None
```

!!! note
    `list()` uses `_paging=1` and `_return_as_object=1` WAPI parameters. The default page size
    is 1000 objects per request. Override with `max_results=N`.

---

## Object references (`_ref`)

Every NIOS WAPI object has a `_ref` field - a stable, opaque identifier used for all
`get`, `update`, `delete`, and function-call operations.

```text
network/ZG5z...base64.../default
zone_auth/ZG5z...base64.../example.com/default
record:a/ZG5z...base64.../web01.example.com/default
```

The ref encodes the object type, internal ID, and key fields. You can always retrieve it
from any model:

```python
zone = await client.dns.zone_auth.find_one(fqdn="example.com", view="default")
if zone:
    print(zone._ref)  # e.g. zone_auth/ZG5z.../example.com/default
```

---

## Filtering

All `list()` and `find_one()` calls accept filter keyword arguments that map to WAPI search
modifiers.

### Exact match

```python
# Exact match: fqdn=example.com
zones = await client.dns.zone_auth.list(fqdn="example.com").all()
```

### Substring / pattern match

```python
# name contains "web"
records = await client.dns.record_a.list(name__like="web").all()
```

### Comparison operators

```python
# IP >= 10.0.0.100
addrs = await client.ipam.ipv4address.list(ip_address__gte="10.0.0.100").all()
```

### Negation

```python
# comment is not empty
networks = await client.ipam.network.list(comment__not="").all()
```

### Extensible attribute search

```python
# EA "Site" = "London"
networks = await client.ipam.network.list(extattr_Site="London").all()
```

### Available filter operators

| Suffix | WAPI operator | Example |
|---|---|---|
| *(none)* | exact match | `view="default"` |
| `__like` | case-insensitive substring | `name__like="web"` |
| `__gte` | greater than or equal | `ip_address__gte="10.0.0.0"` |
| `__lte` | less than or equal | `ip_address__lte="10.255.255.255"` |
| `__not` | not equal | `comment__not=""` |
| `extattr_*` | EA value match | `extattr_Site="London"` |

---

## Controlling returned fields

By default, each resource returns a predefined set of fields (the `_default_return_fields` for that
resource). You can override this in two ways.

### Replace default fields

```python
zones = await client.dns.zone_auth.list(
    return_fields=["fqdn", "view", "comment"],
).all()
```

### Extend default fields

```python
zones = await client.dns.zone_auth.list(
    return_fields_plus=["grid_primary", "grid_secondary"],
).all()
```

!!! note
    `return_fields_plus` is additive - it appends to the resource's defaults rather than
    replacing them. Use it when you want the usual fields *plus* a few extras.

---

## Finding a single object

`find_one()` runs a `list_page(max_results=1)` and returns the first result or `None`:

```python
async with NiosClient() as client:
    zone = await client.dns.zone_auth.find_one(
        fqdn="example.com",
        view="default",
    )
    if zone is None:
        print("Zone not found")
    else:
        print(zone._ref)
```

---

## Get by reference

```python
async with NiosClient() as client:
    ref = "network/ZG5z.../10.10.0.0/24/default"
    network = await client.ipam.network.get(ref)
    print(network.network, network.comment)
```

---

## Create, update, delete

```python
async with NiosClient() as client:
    # Create
    rec = await client.dns.record_a.create({
        "name": "web01.example.com",
        "view": "default",
        "ipv4addr": "10.10.0.5",
        "comment": "web server",
    })
    ref = rec._ref

    # Update
    updated = await client.dns.record_a.update(ref, {"comment": "primary web server"})

    # Delete
    await client.dns.record_a.delete(ref)
```

### Operations an object type does not support

WAPI restricts operations per object type: `allrecords` is a read-only aggregate,
`grid` cannot be deleted, and function-only types such as `dtc` refuse even a read
while still accepting `call_function()`. A grid answers those with
`AdmConProtoError: Operation <op> not allowed for <type>`.

The SDK records each type's restrictions (read from a NIOS 9.1 / WAPI 2.14 grid's
`?_schema`) and raises before sending the request:

```python
from ibx_nios_sdk import UnsupportedOperationError

async with NiosClient() as client:
    try:
        await client.dns.allrecords.create({"name": "web01.example.com"})
    except UnsupportedOperationError as exc:
        print(exc.wapi_type, exc.operation)  # allrecords create
```

`list()` raises on the call itself, not on the first iteration, and `set_extattrs()`
is gated with `update()`. On a grid whose restrictions differ from the table, pass
`enforce_restrictions=False` to send the request and let the grid decide:

```python
async with NiosClient(enforce_restrictions=False) as client:
    await client.dtc.dtc.list().all()  # raises BadRequestError from the grid instead
```

---

## Calling WAPI functions

WAPI exposes "function" endpoints (`?_function=<name>`) on specific object types. The SDK
provides a generic `call_function()` method plus typed wrappers for the most common functions.

### Generic call

```python
async with NiosClient() as client:
    ref = "zone_auth/ZG5z.../example.com/default"
    result = await client.dns.zone_auth.call_function(
        ref,
        "copyzonerecords",
        zone="source.example.com",
        copy_all_records=True,
    )
```

### Typed wrapper examples

```python
async with NiosClient() as client:
    # Copy all records from one zone into another (creates the target if missing).
    zone = await client.dns.zone_auth.find_one(fqdn="new.example.com", view="default")
    await client.dns.zone_auth.copy_zone_records(
        zone._ref,
        source_zone="old.example.com",
        copy_all_records=True,
    )

    # Lock a zone to prevent edits while a migration runs; unlock when done.
    await client.dns.zone_auth.lock_unlock_zone(zone._ref, lock=True)
    try:
        # ... perform migration ...
        pass
    finally:
        await client.dns.zone_auth.lock_unlock_zone(zone._ref, lock=False)

    # Allocate three IPs from a /24 in one call.
    net_ref = "network/ZG5z.../10.10.0.0/24/default"
    result = await client.ipam.network.next_available_ip(net_ref, num=3)
    ips = result["ips"]           # list[str]

    # Carve out a new /26 from a container.
    cont_ref = "networkcontainer/ZG5z.../10.10.0.0/16/default"
    new_net = await client.ipam.networkcontainer.next_available_network(
        cont_ref, cidr=26, num=1,
    )
```

### All typed wrappers

| Method | WAPI function |
|---|---|
| `client.dns.zone_auth.copy_zone_records(ref, source_zone=...)` | `copyzonerecords` |
| `client.dns.zone_auth.lock_unlock_zone(ref, lock=True)` | `lock_unlock_zone` |
| `client.ipam.network.next_available_ip(ref, num=1)` | `next_available_ip` |
| `client.ipam.networkcontainer.next_available_network(ref, cidr=24)` | `next_available_network` |
| `client.ipam.ipv6network.next_available_ip(ref, num=1)` | `next_available_ip` |
| `client.ipam.ipv6networkcontainer.next_available_network(ref, cidr=64)` | `next_available_network` |
| `client.dhcp.range.next_available_ip(ref, num=1)` | `next_available_ip` |
| `client.dhcp.ipv6range.next_available_ip(ref, num=1)` | `next_available_ip` |
| `client.grid.grid.restart_services(ref, ...)` | `restartservices` |
| `client.grid.member.restart_services(ref, ...)` | `restartservices` |
| `client.grid.grid_servicerestart_group.restart_services(ref)` | `restartservices` |

---

## Setting extensible attributes

```python
async with NiosClient() as client:
    ref = "network/ZG5z.../10.10.0.0/24/default"
    await client.ipam.network.set_extattrs(
        ref,
        Site="London",
        Owner="networking-team",
    )
```

---

## Error handling

The SDK raises `NiosError` (or a subclass) for all API errors. Catch the base class to handle
any SDK error, or catch specific subclasses for fine-grained handling.

```python
from ibx_nios_sdk._exceptions import NiosError

async with NiosClient() as client:
    try:
        zone = await client.dns.zone_auth.get("zone_auth/bad-ref")
    except NiosError as exc:
        print(f"NIOS error {exc.status_code}: {exc.message}")
```

Common exception types:

| Exception | When raised |
|---|---|
| `NiosError` | Base class for all SDK errors |
| `AuthenticationError` | 401 Unauthorized - bad credentials or expired session |
| `NotFoundError` | 404 - object ref does not exist |
| `ConflictError` | 409 - object already exists or constraint violation |
| `BadRequestError` | 400 - WAPI rejected the request payload |
| `RateLimitError` | 429 - too many requests |
| `ServerError` | 5xx - server-side failure |
| `NiosConnectionError` | TLS, DNS, or connect failure before any response |
| `ValidationError` | Response did not match the expected pydantic model |
| `UnsupportedOperationError` | Object type does not support the operation - raised before the request |

---

## Concurrency and connection reuse

The SDK is fully async and safe to drive from many concurrent coroutines. A few practical
rules keep a workload healthy against a real NIOS grid.

### Share one `NiosClient` across coroutines

The client owns a single `httpx.AsyncClient` (connection pool) and - in session mode - a
single `ibapauth` cookie. Sharing one instance means all concurrent requests reuse the TCP
connection pool and the already-authenticated session.

```python
async with NiosClient() as client:
    async def create_record(name: str, ip: str):
        return await client.dns.record_a.create({
            "name": name, "view": "default", "ipv4addr": ip,
        })

    results = await asyncio.gather(*[
        create_record(f"host{i:03}.example.com", f"10.0.0.{i}")
        for i in range(1, 51)
    ])
```

!!! warning
    Do **not** create a fresh `NiosClient` per coroutine - you will trigger 50 parallel
    `/grid/session` logins and blow past NIOS's session-count limit.

### Bound parallelism

NIOS Grid Managers are not designed for unlimited concurrency. Keep simultaneous
write-style requests in double digits; reads tolerate more but still benefit from a cap.
Use `asyncio.Semaphore` when fanning out large workloads:

```python
sem = asyncio.Semaphore(10)                  # at most 10 in-flight at once

async def bounded_create(payload):
    async with sem:
        return await client.dns.record_a.create(payload)

await asyncio.gather(*(bounded_create(p) for p in payloads))
```

### Timeout and retry interaction

`timeout` is **per request**, not per workflow. A workflow that issues 100 requests with
`timeout=30` has no single 30-second cap. `max_retries` governs transient failures
(429, 502, 503, 504) - each retry consumes the same per-request timeout. Budget both:

```python
async with NiosClient(timeout=60.0, max_retries=5) as client:
    # Up to 60s per HTTP attempt, with 5 retries on 429/5xx.
    ...
```

### Don't block the event loop

Calls inside `async def` must be non-blocking. Disk I/O, CPU-heavy pydantic work on huge
result sets, and anything that calls a synchronous HTTP library will stall every other
coroutine on that event loop. Offload CPU work with `asyncio.to_thread(...)` and prefer
iterating `list()` over materialising with `.all()` for very large object types.
