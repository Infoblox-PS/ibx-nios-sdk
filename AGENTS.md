# AGENTS.md

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate  # Create/activate venv
pip install -e ".[dev]"          # Install with dev deps
pytest -v                        # Run all tests
pytest tests/_http/ -v           # Run a specific directory
pytest -k "test_retry" -v        # Run tests matching pattern
ruff check .                     # Lint (whole repo, docs/examples included)
ruff format .                    # Format
mypy                             # Type check (strict mode)
```

## Architecture

Async-only SDK built on httpx + pydantic v2. Python 3.11+.

```text
src/ibx_nios_sdk/
├── client.py              # NiosClient - entry point, lazy service init
├── _http.py               # HttpClient - httpx wrapper, session auth, retry
├── _exceptions.py         # NiosError hierarchy
├── _resource.py           # WapiResource - list/get/create/update/delete/call_function
├── _query.py              # Filter/return-fields query-param builder
├── _paging.py             # AsyncPageIterator
├── _common/models.py      # Cross-domain shared models (ExtAttrValue, ...)
└── <domain>/              # Per-WAPI-swagger packages, added in later phases:
    ├── _service.py        #   DomainService with @cached_property per resource
    ├── _<object>.py       #   One resource class per WAPI object type
    └── models/            #   Hand-written pydantic v2 models
```

**Key pattern:** `client.dns.record_a.list(zone="example.com")` → `NiosClient` → `DnsService` → `RecordAResource` → `HttpClient`.

## Key Patterns

- **One HttpClient for all domains** - WAPI is a single base `/wapi/v{version}/`, unlike ibx-uddi-sdk which has per-domain base paths.
- **Session-cookie auth by default** - lazy `/grid/session` login on first request; cookie reused; `/logout` on close. Set `use_session=False` for basic-auth-per-request mode.
- **401 auto-retry** - on 401 (session-mode only), SDK re-logs in once and retries the original request before raising AuthenticationError.
- **Retry** - exponential backoff on 429, 502, 503, 504. 500 is NOT retried (WAPI returns 500 for legitimate validation errors).
- **`_ref` pass-through** - WAPI `_ref` is the object's URL fragment. No short-ID stripping. Resource methods validate ref starts with the wapi_type prefix.
- **Auto-paginated list()** - returns AsyncPageIterator. `list_page()` exposes one-page control.
- **Return fields default** - SDK sends `_return_fields+=<model fields>` by default so the full pydantic model populates. Trim with `return_fields=[..]` or extend with `return_fields_plus=[..]`.
- **Filter operators via kwarg suffix** - `name="x"` exact, `name__like="x"` substring, `name__gte=5` ≥, `name__lte=5` ≤, `name__not="x"` ≠, `extattr_Site="NYC"` extattr filter.
- **Create/Update** - accept Model or dict. Model serialized with `model_dump(exclude_none=True, by_alias=True, exclude={"ref"} | _readonly_fields | _create_only_fields)` on update; create keeps create-only fields.
- **Function calls** - `await resource.call_function(ref, "next_available_ip", num=5)`. Typed wrappers for common functions live on specific resource subclasses. Never gated by restrictions.
- **Per-type operation restrictions** - WAPI refuses operations an object type does not support (`Operation create not allowed for allrecords`). Generated `_restrictions.py` maps wapi_type → restricted ops from the snapshot's `restrictions`; `WapiResource` raises `UnsupportedOperationError` before the request. `NiosClient(enforce_restrictions=False)` opts out; a subclass may set `_restricted_ops` explicitly.
- **TLS verify by default** - `verify=False` or `ca_bundle=...` to opt out. TLS errors wrapped in NiosConnectionError with helpful message.

## Environment Variables

- `NIOS_GRID_URL` - e.g. `https://grid.example.com`
- `NIOS_USERNAME`
- `NIOS_PASSWORD`
- `NIOS_WAPI_VERSION` - optional, default `2.14`
- `IB_LOG_LEVEL=DEBUG` - enable debug logging

## Testing

- All tests async (`asyncio_mode = "auto"`).
- `httpx.MockTransport` for HTTP mocking - handlers are **sync** `def handler(request: httpx.Request) -> httpx.Response`.
- Shared helpers in `tests/conftest.py`: `make_http_client()`, `json_response()`.
- Session-mode handlers must respond to `/grid/session` with `Set-Cookie: ibapauth=...; Path=/`.
- Live integration tests under `tests/integration/` run only when `NIOS_LIVE=1`, and read
  the grid from `NIOS_GRID_URL` / `NIOS_USERNAME` / `NIOS_PASSWORD` (plus optional
  `NIOS_WAPI_VERSION`, `NIOS_VERIFY`). `tests/integration/conftest.py` loads those from a
  git-ignored `.env` (template: `.env.example`) when `NIOS_LIVE` is set; real env vars win.
  Never hardcode a grid address or credential in the repo.
- **Schema conformance** - `tests/fixtures/wapi_schema_v2.14.json` is a compact snapshot of
  `?_schema&_schema_version=2` for every object type. `tests/test_schema_conformance.py`
  fails when a model field's type disagrees with the schema's wire shape (list vs scalar,
  struct vs `_ref` string, int vs str); `tests/test_full_return_fields.py` lists every object
  with its full readable field set. Known schema-vs-wire exceptions live in
  `WIRE_OVERRIDES` in `tests/wapi_schema.py`. Refresh the snapshot from a grid with
  `python tools/refresh_wapi_schema_snapshot.py` (reads `NIOS_*` env vars), then regenerate the
  restriction table with `python tools/refresh_object_restrictions.py`.
- **Restrictions** - each object's `restrictions` list in the snapshot drives
  `src/ibx_nios_sdk/_restrictions.py`. `tests/test_object_restrictions.py` checks the table
  against the snapshot and asserts every restricted op raises without reaching the transport.
  Per-resource mock tests that exercise a restricted op pass `enforce_restrictions=False`.
  The nios-swagger specs are only a fallback source (`--swagger <checkout>/swagger-ui/openspec/v2.14`)
  and disagree with the grid for ~30 types.
- Wire-shape rules for model fields: `is_array` → `list[...]`; struct → `dict[str, Any]`;
  another WAPI object type → `dict[str, Any] | str` (`_ref` string, or inline object for child
  types); `timestamp` → `int`; enum → `Literal[...] | str`.

## CLI & Examples

The `[cli]` optional-dependency group (`pip install 'ibx-nios-sdk[cli]'`) installs
`click` and `click-option-group` and registers 10 `nios-*` console entry points:

```text
nios-csvexport, nios-csvimport, nios-get-file, nios-get-log,
nios-get-supportbundle, nios-grid-backup, nios-grid-restore,
nios-certificate, nios-restart-service, nios-restart-status
```

- Full reference: `docs/cli-utilities.md`
- 22 workflow example scripts live under `docs/examples/` - see `docs/examples-index.md`.
- `docs/examples/manage_dtc_full.py` is the flagship end-to-end DTC workflow.

## Code Style

- **Licence header** - every `.py` file starts with `# SPDX-License-Identifier: Apache-2.0`
  and a `# Copyright (C) <year> Infoblox, Inc.` line (after the shebang, where there is one).
  New files must carry it; `tests/test_license_headers.py` fails otherwise. The SDK is
  Apache-2.0 (permissive, so it can be linked into closed software) - keep new
  dependencies permissive too, and never add a copyleft dependency without asking.
- Line length: 99 (ruff)
- Ruff rules: E, F, I, UP, B, SIM, TCH
- Private modules prefixed with `_` (e.g. `_http.py`, `_resource.py`)
- Public exports only in `__init__.py`
