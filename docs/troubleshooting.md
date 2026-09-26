# Troubleshooting

---

## TLS certificate verification failure

**Symptom:** `httpx.ConnectError` or `ssl.SSLCertVerificationError` when connecting to the Grid.

**Cause:** Most NIOS Grid Managers use a self-signed certificate or an internal CA that is not in
the system trust store.

**Solutions:**

=== "Supply your CA bundle"

    ```python
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
        ca_bundle="/etc/ssl/certs/infoblox-ca.pem",
    ) as client:
        ...
    ```

=== "Disable verification (lab only)"

    ```python
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
        verify=False,
    ) as client:
        ...
    ```

=== "Environment variable"

    ```bash
    # Point httpx at your CA bundle via env var (alternative approach)
    export SSL_CERT_FILE=/path/to/ca-bundle.pem
    ```

!!! warning
    `verify=False` disables all TLS validation. Only use this in isolated lab environments.

---

## 401 Unauthorized

**Symptom:** `AuthenticationError` (HTTP 401) on the first request or mid-session.

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| Wrong username or password | Verify credentials against the NIOS UI |
| Account locked after failed attempts | Unlock in NIOS Admin → Users |
| Session cookie expired during a long-running script | Reconnect by re-entering `async with NiosClient(…)` |
| Using `use_session=False` but password contains special chars | URL-encode or ensure `httpx` Basic auth handles encoding |
| Insufficient admin permissions for the endpoint | Grant the required admin role in NIOS |

```python
from ibx_nios_sdk import AuthenticationError

try:
    async with NiosClient() as client:
        ...
except AuthenticationError as exc:
    print(f"Auth failed: {exc.message}")
```

---

## Retry exhausted

**Symptom:** `NiosError` with message "max retries exceeded" after multiple attempts.

**Cause:** The Grid is overloaded, the connection is being reset, or a 5xx is returned repeatedly.

**Fixes:**

- Increase `max_retries` in the constructor.
- Add a delay between your script's own request loops.
- Check Grid health in NIOS Dashboard.
- Reduce concurrent requests if running multiple coroutines.

```python
async with NiosClient(max_retries=5, timeout=60.0) as client:
    ...
```

---

## Pagination gotchas

**Symptom:** Only the first 1000 objects returned; the rest are missing.

**Cause:** Calling `.list_page()` directly returns a single page. You must paginate or use `.all()`.

```python
# Wrong - only returns first 1000 zones
rows, _ = await client.dns.zone_auth.list_page()

# Correct - iterates all pages
async for zone in client.dns.zone_auth.list():
    process(zone)

# Or collect all at once
zones = await client.dns.zone_auth.list().all()
```

**Symptom:** `list().all()` is very slow for large datasets.

**Fix:** Apply server-side filters to reduce the result set, or process records in the async loop
instead of collecting everything into memory.

```python
# Filter on server side
async for zone in client.dns.zone_auth.list(view="default", zone_format="FORWARD"):
    process(zone)
```

---

## Object not found / wrong ref

**Symptom:** `NotFoundError` (HTTP 404) when fetching by ref, or `ValueError: ref does not match wapi_type`.

**Fixes:**

- Ensure the ref prefix matches the resource type (e.g., `"zone_auth/…"` for `zone_auth.get()`).
- Re-query the object to get a fresh ref - refs can change after upgrade or restore operations.

```python
zone = await client.dns.zone_auth.find_one(fqdn="example.com", view="default")
if zone:
    fresh_ref = zone._ref
```

---

## Operation not allowed for this object type

**Symptom:** `UnsupportedOperationError: WAPI object type 'allrecords' does not support create`,
raised before any request - or, from a grid, `AdmConProtoError: Operation create not allowed for
allrecords`.

**Cause:** WAPI restricts operations per object type. Read-only aggregates (`allrecords`,
`allendpoints`), reports (`capacityreport`, `dhcp:statistics`) and status objects reject every
mutation; singletons such as `grid` reject `delete`; function-only types (`dtc`, `discovery`,
`fedipamop`, `network_discovery`) reject even a read while still accepting `call_function()`.
The SDK checks the object type's restrictions, recorded from a NIOS 9.1 / WAPI 2.14 grid, and
raises locally instead of making the call.

**Fixes:**

- Use the operation the type supports - often a function call, or a mutation on the parent
  object (create `record:a` rather than `allrecords`).
- On a grid whose restrictions differ from the recorded table, pass
  `NiosClient(enforce_restrictions=False)` and let the grid decide.

```python
from ibx_nios_sdk import UnsupportedOperationError

try:
    await client.dtc.dtc.list().all()
except UnsupportedOperationError as exc:
    print(exc.wapi_type, exc.operation)  # dtc read
```

---

## Enabling debug logging

Set `IB_LOG_LEVEL=DEBUG` to see full HTTP request/response details including headers and body:

```bash
IB_LOG_LEVEL=DEBUG python my_script.py
```

Or in code:

```python
import logging
logging.getLogger("ibx_nios_sdk").setLevel(logging.DEBUG)
logging.basicConfig()
```

This will print the WAPI URL, parameters, request payload, status code, and response body for
every call - very useful for diagnosing unexpected errors.

---

## WAPI version mismatch

**Symptom:** `BadRequestError` on create/update, or fields silently missing from responses.

**Cause:** The WAPI version specified in the client doesn't match the Grid's NIOS version.

**Fix:** Use `wapi_version` matching your Grid. Check the Grid's WAPI version at
`https://gm.example.com/wapi/v2.14/?_schema`.

```python
async with NiosClient(wapi_version="2.11") as client:
    ...
```

---

## Common WAPI error codes

NIOS returns a JSON error body with a top-level `code`, `text`, and optional `Error` fields.
The SDK wraps these in `NiosError` subclasses and exposes `status_code`, `wapi_code`,
`wapi_text`, `response_body`, and `request_url` on the exception. The table below maps the
most common codes you will see in logs.

| NIOS code | HTTP | Meaning | Typical cause / fix |
|---|---|---|---|
| `Client.Ibap.Proto.AdmConProtoError` | 400 | Malformed request | Unknown field/argument for this WAPI version. Use `return_fields=` to avoid sending fields your grid does not know. |
| `Client.Ibap.Data` | 400 | Validation error | Payload violates an object rule (e.g. invalid IP, missing required field). Inspect `exc.wapi_text`. |
| `Client.Ibap.Data.Conflict` | 409 | Duplicate or conflict | Object already exists, or a referenced object is in use. Use `find_one()` first, or catch `ConflictError`. |
| `Client.Ibap.Proto.NotFound` | 404 | Ref does not exist | Stale ref (object deleted or renamed after upgrade/restore). Re-query for a fresh ref. |
| `Client.Ibap.LicenseExpired` | 400 | License missing/expired | Feature requires a grid license (e.g. DTC, Threat Insight). Check `client.grid.license_gridwide.list()`. |
| `Client.Ibap.Proto.AdmConAuthError` | 401 | Auth failure | Bad credentials, locked account, or expired session cookie. SDK auto-retries sessions once. |
| `Client.Ibap.Proto.InsufficientPrivileges` | 403 | Permission denied | Admin role lacks the required permission. Grant the role in NIOS Admin → Groups. |
| `Client.Ibap.Proto.TooManyRequests` | 429 | Rate limited | SDK retries automatically with exponential backoff. Reduce concurrency if persistent. |
| *(any)* | 500 | Server-side validation or bug | **Not retried** - NIOS returns 500 for legitimate validation failures. Inspect the payload. |
| *(any)* | 502 / 503 / 504 | Transient | Retried with backoff. Check Grid Manager health if repeated. |

```python
from ibx_nios_sdk._exceptions import NiosError

try:
    await client.dns.record_a.create({...})
except NiosError as exc:
    print(exc.status_code, exc.wapi_code, exc.message)
    print(exc.wapi_text)          # NIOS-provided human-readable text
    print(exc.response_body)      # raw response body string
```

---

## Getting help

- Check the [Common Patterns](common-patterns.md) page for filter syntax and return_fields usage.
- Open an issue at [github.com/Infoblox-PS/ibx-nios-sdk](https://github.com/Infoblox-PS/ibx-nios-sdk).
- Enable `DEBUG` logging and include the output in your issue report.
