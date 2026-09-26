# Migration from infoblox-client

[infoblox-client](https://github.com/infobloxopen/infoblox-client) is the legacy synchronous Python
library for NIOS WAPI. This page covers how to migrate existing scripts to ibx-nios-sdk.

---

## Key differences at a glance

| Aspect | infoblox-client (old) | ibx-nios-sdk (new) |
|---|---|---|
| Execution model | Synchronous | `async/await` only |
| Entry point | `ibx.client.InfobloxConnector(…)` | `NiosClient(…)` |
| Auth | Basic auth hardcoded | Session auth by default; Basic with `use_session=False` |
| Return types | Raw `dict` / `list` | Typed Pydantic models |
| Ref handling | `_ref` as raw string | Same - `_ref` is still a plain string |
| Pagination | Manual, no built-in helper | `AsyncPageIterator` with `.all()` |
| Retry | None | Built-in exponential back-off (`max_retries=3`) |
| Error handling | Raises `Exception` with message string | Typed exception hierarchy (`NiosError` subclasses) |
| Field selection | `return_fields=` list | `return_fields=` or `return_fields_plus=` |

---

## Method mapping

| infoblox-client | ibx-nios-sdk | Notes |
|---|---|---|
| `connector.get_object("record:a", {"name": "web"})` | `await client.dns.record_a.list(name="web").all()` | Returns typed models, not dicts |
| `connector.create_object("record:a", {"name": …})` | `await client.dns.record_a.create({…})` | Returns typed model |
| `connector.update_object(ref, {"comment": …})` | `await client.dns.record_a.update(ref, {…})` | `ref` is still a plain string |
| `connector.delete_object(ref)` | `await client.dns.record_a.delete(ref)` | - |
| `connector.call_func("next_available_ip", ref, {})` | `await client.ipam.network.next_available_ip(ref, num=1)` | Typed wrapper returns dict |

---

## Before / after: list zones

**Before (infoblox-client):**

```python
import ibx.client as ibx

conn = ibx.InfobloxConnector(
    host="gm.example.com",
    username="admin",
    password="infoblox",
    ssl_verify=False,
)
zones = conn.get_object("zone_auth", {"view": "default"})
for z in zones:
    print(z["fqdn"])
```

**After (ibx-nios-sdk):**

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
        verify=False,
    ) as client:
        async for zone in client.dns.zone_auth.list(view="default"):
            print(zone.fqdn)  # typed attribute, not dict key

asyncio.run(main())
```

---

## Before / after: create A record

**Before:**

```python
ref = conn.create_object("record:a", {
    "name": "web01.example.com",
    "view": "default",
    "ipv4addr": "10.0.0.5",
})
print(ref)  # raw _ref string
```

**After:**

```python
async with NiosClient() as client:
    rec = await client.dns.record_a.create({
        "name": "web01.example.com",
        "view": "default",
        "ipv4addr": "10.0.0.5",
    })
    print(rec._ref)  # attribute on typed model
```

---

## Before / after: next available IP

**Before:**

```python
result = conn.call_func("next_available_ip", ref, {"num": 1})
ip = result["ips"][0]
```

**After:**

```python
async with NiosClient() as client:
    result = await client.ipam.network.next_available_ip(ref, num=1)
    ip = result["ips"][0]
```

---

## Running synchronously

ibx-nios-sdk is async-only. If you need to call it from synchronous code:

```python
import asyncio
from ibx_nios_sdk import NiosClient

def list_zones_sync():
    async def _inner():
        async with NiosClient() as client:
            return await client.dns.zone_auth.list().all()

    return asyncio.run(_inner())
```

!!! warning
    Do not call `asyncio.run()` from inside an already-running event loop (e.g., Jupyter notebooks
    or FastAPI handlers). In those contexts, use `await` directly.

---

## Notes on `_ref` strings

The `_ref` format has not changed - refs from older infoblox-client scripts remain valid in
ibx-nios-sdk. You can pass them directly to `get()`, `update()`, `delete()`, and typed function
wrappers.

```python
# ref obtained from infoblox-client or from the NIOS UI
old_ref = "record:a/ZG5z.../web01.example.com/default"
rec = await client.dns.record_a.get(old_ref)
```

!!! note
    The SDK validates the ref prefix matches the resource type. If you call
    `client.dns.record_a.get("network/…")`, you'll get a `ValueError` immediately without a
    network round-trip.

!!! note
    The SDK also knows which operations each object type supports. Where infoblox-client
    forwarded the call and surfaced NIOS's `Operation <op> not allowed for <type>`, this SDK
    raises `UnsupportedOperationError` up front - so a script that created `allrecords` or
    listed `dtc` now fails locally and immediately. Pass
    `NiosClient(enforce_restrictions=False)` to restore the old round-trip behaviour.
