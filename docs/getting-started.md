# Getting Started

## Installation

ibx-nios-sdk requires **Python 3.11 or later**.

```bash
pip install ibx-nios-sdk
```

Core dependencies installed automatically:

| Package | Version | Purpose |
|---|---|---|
| `httpx` | ≥ 0.27 | Async HTTP client |
| `pydantic` | ≥ 2 | Data validation and typed models |
| `python-dateutil` | ≥ 2.8.2 | Date parsing for DHCP lease timestamps |

---

## Authentication

NIOS WAPI supports two authentication modes.

### Session auth (default)

When you enter the async context manager (`async with NiosClient(...) as client:`), the SDK
posts credentials to `/grid/session` to obtain a session cookie. That cookie is sent with every
subsequent request. On exit, `/logout` is called automatically.

This is the recommended mode - session auth is faster for many API calls and avoids sending
credentials in every request header.

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
    ) as client:
        zones = await client.dns.zone_auth.list().all()
        print(f"{len(zones)} authoritative zones")

asyncio.run(main())
```

### Basic auth (stateless)

Pass `use_session=False` to send HTTP Basic credentials on every request. Useful for scripts that
make a single API call, or when session cookies are problematic in your environment.

```python
async with NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
    use_session=False,
) as client:
    ...
```

!!! note
    Even with `use_session=False`, you can still use the async context manager - the SDK simply
    skips the session login/logout cycle.

---

## First API call

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def list_zones():
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
    ) as client:
        async for zone in client.dns.zone_auth.list(view="default"):
            print(zone.fqdn, zone.zone_format)

asyncio.run(list_zones())
```

---

## Using environment variables

You can avoid hardcoding credentials by setting environment variables before running your script:

```bash
export NIOS_GRID_URL="https://gm.example.com"
export NIOS_USERNAME="admin"
export NIOS_PASSWORD="infoblox"
export NIOS_WAPI_VERSION="2.14"   # optional; defaults to 2.14
```

Then construct the client with no arguments:

```python
async with NiosClient() as client:
    ...
```

---

## TLS certificate verification

By default the SDK verifies the Grid Manager's TLS certificate against the system trust store.
Most production Grids use self-signed or internal CA certificates - the SDK will raise a clear
error if verification fails.

### Option 1 - Supply your CA bundle

```python
async with NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
    ca_bundle="/path/to/infoblox-ca.pem",  # or a directory of PEM files
) as client:
    ...
```

### Option 2 - Disable verification (lab use only)

```python
async with NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
    verify=False,
) as client:
    ...
```

!!! warning
    `verify=False` disables all certificate validation. Never use this in production. Python will
    emit `InsecureRequestWarning` from `urllib3` when this is set.

---

## Choosing a WAPI version

The SDK defaults to WAPI **2.14**. If your Grid is on a different NIOS version, set the
version explicitly:

```python
async with NiosClient(
    grid_url="https://gm.example.com",
    username="admin",
    password="infoblox",
    wapi_version="2.11",
) as client:
    ...
```

Or via env var: `NIOS_WAPI_VERSION=2.11`.

!!! note
    Some resource fields are only available in newer WAPI versions. If you get unexpected
    validation errors on object creation, check the WAPI schema for your NIOS version.
