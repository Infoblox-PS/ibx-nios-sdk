# Configuration

## NiosClient constructor

```python
from ibx_nios_sdk import NiosClient

client = NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
    wapi_version="2.14",
    use_session=True,
    verify=True,
    ca_bundle=None,
    timeout=30.0,
    max_retries=3,
    enforce_restrictions=True,
)
```

### Parameter reference

| Parameter | Type | Default | Description |
|---|---|---|---|
| `grid_url` | `str \| None` | `None` | Base URL of the Grid Manager (e.g. `https://gm.example.com`). Falls back to `NIOS_GRID_URL` env var. Required. |
| `username` | `str \| None` | `None` | NIOS admin username. Falls back to `NIOS_USERNAME`. Required. |
| `password` | `str \| None` | `None` | NIOS admin password. Falls back to `NIOS_PASSWORD`. Required. |
| `wapi_version` | `str \| None` | `None` | WAPI version string, e.g. `"2.14"`. Falls back to `NIOS_WAPI_VERSION`, then SDK default (`2.14`). |
| `use_session` | `bool` | `True` | When `True`, log in at context manager entry and log out on exit. When `False`, use HTTP Basic auth on every request. |
| `verify` | `bool \| str \| Path` | `True` | TLS verification. `True` = system CA store. `False` = disable (lab only). `str`/`Path` = path to CA bundle. |
| `ca_bundle` | `str \| Path \| None` | `None` | Convenience alias: if set, overrides `verify` with this path. |
| `timeout` | `float` | `30.0` | HTTP request timeout in seconds. |
| `max_retries` | `int` | `3` | Number of automatic retries on transient network errors (5xx, connection resets). |
| `enforce_restrictions` | `bool` | `True` | When `True`, refuse an operation the object type's WAPI schema restricts and raise `UnsupportedOperationError` without a request. `False` sends it and lets the grid answer. |

---

## Environment variables

| Variable | Corresponds to | Example |
|---|---|---|
| `NIOS_GRID_URL` | `grid_url` | `https://gm.example.com` |
| `NIOS_USERNAME` | `username` | `admin` |
| `NIOS_PASSWORD` | `password` | `infoblox` |
| `NIOS_WAPI_VERSION` | `wapi_version` | `2.14` |
| `IB_LOG_LEVEL` | SDK log level | `DEBUG`, `INFO`, `WARNING` |

!!! note
    Constructor arguments always take priority over environment variables. The environment is
    only consulted when the corresponding argument is `None`.

---

## Authentication modes

The SDK supports two authentication modes, controlled by the `use_session` flag.

### Session-cookie auth (default, `use_session=True`)

- Lazy `POST /grid/session` on the first request; NIOS returns an `ibapauth` cookie.
- The cookie is reused across every subsequent request - one login per client instance.
- `POST /logout` is called on context-manager exit (or `close()`).
- On `401 Unauthorized`, the SDK re-authenticates **once** and transparently retries the
  original request before raising `AuthenticationError`. This handles NIOS's idle-session timeout
  without any caller-side bookkeeping.

Use session auth for anything that issues more than one or two requests - it eliminates the
per-request auth round-trip and matches how the NIOS UI itself behaves.

### HTTP Basic auth (`use_session=False`)

- Sends `Authorization: Basic …` on every request; no `/grid/session` call, no cookie.
- No server-side session state, so no 401 auto-retry (each request authenticates fresh).
- Appropriate for one-shot scripts, health probes, or environments where creating a session
  record on the Grid is undesirable (auditing, session-count limits, service accounts).

```python
async with NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
    use_session=False,       # Basic auth on every request
) as client:
    result = await client.grid.grid.list().all()
```

### Credential hygiene

- Prefer environment variables (`NIOS_USERNAME` / `NIOS_PASSWORD`) or a secrets manager over
  hard-coded literals. Avoid committing `.env` files to source control.
- Debug logging (`IB_LOG_LEVEL=DEBUG`) prints request URLs, status codes, and timings. If
  you enable `httpx` wire-level logging separately it may include the `Authorization` header
  or `ibapauth` cookie - keep those logs out of shared channels.
- Use a dedicated NIOS admin account with the minimum role required for the workflow rather
  than a shared superuser - NIOS's permission system is enforced at the WAPI layer.

---

## Log level

Set `IB_LOG_LEVEL=DEBUG` to see every HTTP request and response:

```bash
IB_LOG_LEVEL=DEBUG python my_script.py
```

Supported levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (Python logging standard).

---

## Context manager lifecycle

The recommended way to use `NiosClient` is as an async context manager:

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
    ) as client:
        # Session is established here (POST /grid/session)
        zone = await client.dns.zone_auth.find_one(fqdn="example.com", view="default")
        if zone:
            print(zone._ref)
        # Session is closed here (POST /logout)

asyncio.run(main())
```

On context exit, the SDK calls `/logout` even if an exception was raised inside the block.

### Without context manager

If you need to manage the session manually:

```python
client = NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
)
await client.__aenter__()
try:
    ...
finally:
    await client.__aexit__(None, None, None)
```

!!! warning
    Always call `__aexit__` (or use `async with`) to avoid leaving orphaned sessions on the Grid.

---

## Putting it all together (env-based config)

```bash
# .env (load with python-dotenv or export manually)
NIOS_GRID_URL=https://gm.corp.example.com
NIOS_USERNAME=svc-automation
NIOS_PASSWORD=s3cret!
NIOS_WAPI_VERSION=2.14
IB_LOG_LEVEL=INFO
```

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    # All config from environment
    async with NiosClient() as client:
        networks = await client.ipam.network.list(
            network_view="default"
        ).all()
        print(f"Found {len(networks)} networks")

asyncio.run(main())
```
