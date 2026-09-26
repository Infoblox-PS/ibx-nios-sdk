# ibx-nios-sdk - Design Spec

- **Date:** 2026-04-17
- **Status:** Approved for planning
- **Target:** `ibx-nios-sdk` v0.1.0, a Python SDK for Infoblox NIOS WAPI v2.14

## Summary

An async-only Python SDK that wraps the Infoblox NIOS WAPI in the same spirit as `ibx-uddi-sdk`: one entry-point client, per-domain services accessed as attributes, `@cached_property` lazy init, hand-written pydantic v2 models, and an `httpx` transport. Covers all 17 WAPI swagger surfaces (dns, dhcp, ipam, grid, rpz, dtc, threatprotection, threatinsight, security, smartfolder, acl, cloud, discovery, federatedrealms, microsoftserver, notification, misc).

Divergences from `ibx-uddi-sdk` are driven by WAPI's different shape: session-cookie or basic auth (not API key), `_ref`-based object identifiers (not short UUIDs), shared `/wapi/v2.14/` base path across all domains (not per-domain bases), and WAPI "function calls" on objects (e.g. `next_available_ip`).

## Decisions

| # | Decision | Choice |
|---|----------|--------|
| 1 | Scope for v0.1 | All 17 swagger domains |
| 2 | Auth model | Session cookie (default) + basic-auth mode, user-selectable |
| 3 | Sync/async | Async-only, `httpx.AsyncClient` |
| 4 | `_ref` surface | Pass-through `_ref` strings + `find_one(**filters)` helper |
| 5 | Model generation | Hand-written pydantic v2 models, swaggers used as reference |
| 6 | Pagination default | Auto-paginate via `AsyncPageIterator` + `list_page()` escape hatch |
| 7 | Function calls | Named methods for common functions + generic `call_function()` fallback |
| 8 | Exception hierarchy | HTTP-status-based (`NiosError` base → Auth/NotFound/BadRequest/Conflict/RateLimit/Server/Validation) |
| 9 | TLS verification | Verify by default; accept `verify=False` or `ca_bundle=` with helpful error |
| 10 | WAPI version | Default `2.14`, user-configurable via `wapi_version=` |
| 11 | `_return_fields` default | Auto-send `_return_fields+=<model fields>`; `return_fields=` trims, `return_fields_plus=` extends |
| 12 | Naming | Project `ibx-nios-sdk`, package `ibx_nios_sdk`, client class `NiosClient` |

## Non-Goals

- No sync API surface in v0.1. Revisit if there is demand.
- No auto-detection of Grid WAPI version (users set `wapi_version=`).
- No code generation from swagger. Swaggers are a reference, not a build input.
- No built-in caching of list/get responses. Callers cache if they need to.
- No ORM-style "save the object I mutated" behavior. Explicit `update(ref, fields)` only.

## Architecture

```
src/ibx_nios_sdk/
├── __init__.py              # public exports: NiosClient + exceptions
├── client.py                # NiosClient entry point; lazy service init
├── _http.py                 # HttpClient: httpx.AsyncClient wrapper, auth, retry, return_fields
├── _exceptions.py           # NiosError hierarchy
├── _resource.py             # WapiResource base (list/list_page/find_one/get/create/update/delete/call_function)
├── _paging.py               # AsyncPageIterator for transparent multi-page iteration
├── _version.py              # WAPI version constants; default "2.14"
├── _common/
│   ├── __init__.py
│   └── models.py            # ExtAttr, ExtAttrValue, cross-domain shared types
│
├── dns/                     # one package per WAPI swagger (17 total)
│   ├── __init__.py
│   ├── _service.py          # DnsService, @cached_property per resource
│   ├── _record_a.py         # one file per WAPI object type
│   ├── _zone_auth.py
│   └── models/
│       ├── __init__.py
│       ├── record_a.py      # pydantic v2 models (hand-written)
│       └── _shared.py       # domain-local nested types + enums
├── dhcp/
├── ipam/
├── grid/
├── rpz/
├── dtc/
├── threatprotection/
├── threatinsight/
├── security/
├── smartfolder/
├── acl/
├── cloud/
├── discovery/
├── federatedrealms/
├── microsoftserver/
├── notification/
└── misc/                    # includes fileop

schemas/v2.14/*.json         # NIOS swagger JSON snapshots, committed for reference/diffing
```

**Primary access pattern:**

```python
async with NiosClient(grid_url="https://grid.example.com",
                      username="admin", password="...") as client:
    async for rec in client.dns.record_a.list(zone="example.com"):
        ...
```

Resolution: `NiosClient` → `DnsService` (cached_property) → `RecordAResource` (cached_property) → `HttpClient` (single shared instance).

All 17 domains share **one** `HttpClient` bound to `/wapi/v{version}/`. This is different from `ibx-uddi-sdk`, which deduplicates clients across multiple base paths.

## HTTP Client & Auth

### `HttpClient`

- Wraps `httpx.AsyncClient` with `base_url = f"{grid_url.rstrip('/')}/wapi/v{wapi_version}"`.
- Owns the cookie jar and credentials. **Never** places basic-auth credentials in default headers.
- Exposes: `get`, `post`, `put`, `delete`, `request_with_retry`.
- Auto-injects `_return_fields` / `_return_fields+` per call (see §"Return Fields").
- Paginates when callers opt in via `paginate=True` (default for `list()`).

### Session mode (default)

1. On first call, lazily `login()`: `POST /grid/session` with `HTTPBasicAuth(user, pass)`. The resulting `ibapauth` cookie is stored in the httpx cookie jar.
2. Subsequent calls rely on the cookie jar - no re-auth per request.
3. On a 401 response, the SDK makes **one** transparent re-login attempt, retries the original request once, then raises `AuthenticationError` if it still fails.
4. `NiosClient` is an async context manager. `close()` calls `POST /logout` to invalidate the session server-side, then `aclose()` the underlying httpx client.

### Basic-auth mode (`use_session=False`)

- No login call. Every request carries `auth=(user, pass)` via an httpx event hook so credentials stay out of default headers.
- Slower (server re-authenticates each call) and noisier in NIOS audit logs; preserved for one-shot CLI use cases.

### TLS

- `verify=True` by default.
- `NiosClient(ca_bundle=<path>)` passes the path to httpx's `verify=` param.
- `NiosClient(verify=False)` explicit opt-out.
- TLS failures are caught and re-raised as `NiosConnectionError` with message:
  `"TLS verification failed against {host}. For self-signed certs, pass verify=False or ca_bundle=/path/to/ca.pem. Underlying error: {orig}"`

### Retry

- Exponential backoff on HTTP 429, 502, 503, 504.
- Backoff capped at 30 s. Default `max_retries=3`.
- 500 responses are **not** retried - WAPI typically returns 500 for legitimate validation errors, not transient faults.
- `Retry-After` header is honored when present.

### Logging

- Logger name: `ibx_nios_sdk`.
- Level controlled by `IB_LOG_LEVEL` env var at module import time (matches `ibx-uddi-sdk`).
- DEBUG logs request URL and query params. Never logs request/response bodies, cookies, or credentials.

## Resource Base

```python
class WapiResource:
    _wapi_type: ClassVar[str]            # e.g. "record:a", "network"
    _model: ClassVar[type[BaseModel]]
    _default_return_fields: ClassVar[list[str]]   # computed from model fields
    _readonly_fields: ClassVar[set[str]] = set()  # stripped on update

    def __init__(self, client: HttpClient): ...

    async def list(self, *, return_fields=None, return_fields_plus=None,
                   max_results=None, **filters) -> AsyncPageIterator[Model]: ...
    async def list_page(self, *, page_id=None, max_results=1000,
                        return_fields=None, return_fields_plus=None,
                        **filters) -> tuple[list[Model], str | None]: ...
    async def find_one(self, *, return_fields=None, return_fields_plus=None,
                       **filters) -> Model | None: ...
    async def get(self, ref: str, *, return_fields=None,
                  return_fields_plus=None) -> Model: ...
    async def create(self, obj: Model | dict, *,
                     return_fields=None) -> Model: ...
    async def update(self, ref: str, obj: Model | dict, *,
                     return_fields=None) -> Model: ...
    async def delete(self, ref: str) -> str: ...  # returns deleted _ref
    async def call_function(self, ref: str | None, function: str,
                            **kwargs) -> dict: ...
```

### `_ref` rules

- WAPI `_ref` is the object's URL fragment and is passed straight through (`GET {base}/{ref}`). No short-ID stripping like `ibx-uddi-sdk` does.
- Before any mutating call, the SDK asserts `ref.startswith(cls._wapi_type + "/")` and raises `ValueError` otherwise. Catches "passed the wrong resource's ref" bugs early.

### Return fields

- **No user override:** send `_return_fields+=<fields the model declares>` so the response fully populates the pydantic model.
- `return_fields=[...]` → send `_return_fields=<exact list>` (trims, does not add modeled fields).
- `return_fields_plus=[...]` → send `_return_fields+=<modeled fields + extras>`.
- Passing both `return_fields` and `return_fields_plus` → `ValueError`.

### Pagination

- `list()` returns an `AsyncPageIterator` that fetches pages on demand.
- Initial request includes `_paging=1&_max_results=1000&_return_as_object=1`. Follows `next_page_id` until exhausted.
- `await iterator.all()` collects into a `list` when the caller knows the set is small.
- `list_page(page_id=..., max_results=...)` exposes one-page-at-a-time control for users who need it.

### `find_one(**filters)`

- Calls `list()` with `_max_results=1`, returns the first match or `None`.
- Filter kwargs translate to WAPI operators:
  - `name="foo"` → `name=foo` (exact)
  - `name__like="foo"` → `name~=foo` (substring/regex)
  - `name__lte=5`, `name__gte=5`, `name__not="foo"` → `<=`, `>=`, `!=`
  - `extattr_Site="NYC"` → `*Site=NYC`
- Unknown operator suffix → `ValueError`.

### `call_function`

- With `ref`: `POST {base}/{ref}?_function={name}` + body.
- Without `ref` (global functions like grid-level restart): `POST {base}/{wapi_type}?_function={name}`.
- Returns a raw `dict`. Function responses are heterogeneous and not worth modeling generically.
- Typed wrappers (e.g. `network.next_available_ip(ref, num=5)`) live on specific resource subclasses and delegate to `call_function` internally.

### Non-CRUD resources

- Objects that don't fit full CRUD (e.g. `fileop`, which is function-only) subclass `WapiResource` and remove/override methods, or use a plain class with `__init__(self, client: HttpClient)` - same escape hatch `ibx-uddi-sdk` uses.

## Models

Hand-written pydantic v2, one model per WAPI object.

```
dns/models/
├── __init__.py        # re-exports: ZoneAuth, RecordA, ...
├── record_a.py
├── zone_auth.py
└── _shared.py         # domain-local enums + nested types
```

### Conventions

- `model_config = ConfigDict(populate_by_name=True, extra="allow")`. `extra="allow"` is deliberate - protects against forward WAPI field additions.
- Every model carries `_ref: str | None = None` (populated on read, unset on create).
- Python-keyword collisions use trailing underscores with aliases: `view_: str | None = Field(default=None, alias="view")`, same for `type_`.
- Nested objects shared within a domain live in `{domain}/models/_shared.py`.
- Cross-domain shared types (`ExtAttr`, `ExtAttrValue`, common grid enums) live in `src/ibx_nios_sdk/_common/models.py`.
- Enums use `StrEnum`, values hand-copied from swagger `enum` arrays.
- Date/time parsing via `python-dateutil`, matching `ibx-uddi-sdk`.
- Read-only fields are kept on the model for read paths (e.g., `creator`, `last_queried`) and listed in `_readonly_fields` on the resource so they are stripped from update payloads.
- `extattrs: dict[str, ExtAttrValue] | None` - the nested `ExtAttrValue` preserves inheritance metadata; no auto-flattening.

### Swagger workflow

- Swaggers in `schemas/v2.14/*.json` are the starting point, not the final word. Real WAPI behavior diverges (undocumented fields, enum drift, required-vs-optional mismatches).
- Each domain has a `NOTES.md` documenting known swagger-vs-reality deltas discovered during implementation.
- When future NIOS versions ship new swaggers, the committed snapshots let us diff and update models deliberately.

### Volume estimate

~300 object types across 17 domains. Rough per-domain counts: dns ~30, dhcp ~20, ipam ~25, grid ~40, rpz ~15, dtc ~20, others 5–15 each. This is a floor; grid and dns may surface additional sub-object types during implementation.

## Create / Update / Delete Semantics

### Create

- `POST {base}/{wapi_type}` with `?_return_as_object=1` always, so the created object comes back populated.
- Accepts `Model` or `dict`.
- `Model` → serialize with `model_dump(exclude_none=True, by_alias=True, exclude={"ref"})`.
- `exclude_none=True` is critical - WAPI distinguishes `null` from "field absent" for many fields.

### Update (PUT)

- WAPI uses **PUT** for updates, but PUT in WAPI is effectively merge-patch (partial bodies are accepted).
- Accepts `Model` or `dict`.
- `Model` → `model_dump(exclude_none=True, by_alias=True, exclude={"ref"} | _readonly_fields)`.
- Caller supplies only the fields they want to change. The SDK does **not** read-modify-write.

### Delete

- `DELETE {base}/{ref}` returns the deleted `_ref` string. The SDK returns that string.

### Extensible attributes

- WAPI shape: `{"extattrs": {"Site": {"value": "NYC"}, ...}}`.
- Models expose `extattrs: dict[str, ExtAttrValue] | None`.
- Convenience helper on every resource: `await resource.set_extattrs(ref, Site="NYC", Owner="net-eng")` wraps an `update(ref, {"extattrs": {...}})`.

### Inheritance fields

- DHCP/IPAM objects support inherited values (e.g. `lease_time` inherits from parent network).
- Default `list`/`get` do **not** request inheritance metadata (smaller payloads).
- Users opt in via `return_fields_plus=["lease_time.inheritance_source"]`.
- Models accept both shapes via union types: `int | InheritedInt`.

## Exception Hierarchy

```
NiosError                     # base
├── NiosConnectionError       # TLS failures, DNS failures, connect timeouts
├── AuthenticationError       # 401
├── NotFoundError             # 404
├── BadRequestError           # 400
├── ConflictError             # 409
├── RateLimitError            # 429
├── ServerError               # 5xx (except 502/3/4 during retry)
└── ValidationError           # pydantic parse failure on response
```

All exceptions carry `status_code`, `wapi_code`, `wapi_text`, `request_url` attributes when available.

## Environment Variables

- `NIOS_GRID_URL` - Grid URL (e.g. `https://grid.example.com`)
- `NIOS_USERNAME`
- `NIOS_PASSWORD`
- `NIOS_WAPI_VERSION` - optional, default `2.14`
- `IB_LOG_LEVEL` - shared convention with `ibx-uddi-sdk`

Constructor arguments always take precedence over env vars.

## Tooling

- `pyproject.toml` with setuptools backend.
- Python 3.11+.
- Runtime deps: `httpx>=0.27`, `pydantic>=2`, `python-dateutil>=2.8.2`.
- Dev deps: `pytest>=8`, `pytest-asyncio>=0.24`, `pytest-cov>=5`, `mypy>=1.10`, `ruff>=0.5`.
- Ruff rules: `E, F, I, UP, B, SIM, TCH`; line length 99; ignores `E501, TC001, TC002, TC003, SIM105`.
- Mypy strict mode on `ibx_nios_sdk`.
- `py.typed` marker shipped.
- License: Apache-2.0.

## Testing

- `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`).
- `httpx.MockTransport` for all HTTP mocking. No `responses`/`vcr.py`/etc.
- Shared helpers in `tests/conftest.py`: `make_client()`, `mock_wapi_response()`, `mock_paginated_response()`.
- Test layout mirrors `src/`: `tests/dns/test_record_a.py`, etc.
- Cross-cutting behaviors (pagination, `_ref` validation, auth retry, TLS error wrapping, retry backoff, `_return_fields` injection, `call_function`, query-operator translation) each get a dedicated test module under `tests/_http/`.
- Integration tests live in `tests/integration/` and are opt-in (`RUN_INTEGRATION=1`). Skipped by default. Used pre-release against a real Grid.
- Coverage target: ≥85% unit-test coverage enforced in CI.

## Examples

`examples/` at repo root. One runnable script per workflow:

- `00_connect_and_login.py`
- `01_create_a_record.py`
- `02_next_available_ip.py`
- `03_bulk_import_csv.py`
- `04_restart_services.py`
- `05_paginate_large_zone.py`
- `06_extattrs_and_filters.py`
- `07_rpz_feed.py`
- Additional per-domain examples added as domains land.

Every example reads credentials from env, runs, prints result. Tested manually against a lab Grid before each release.

## Docs

- **Zensical** for the documentation site, configured via `zensical.toml` at repo root (matches `ibx-uddi-sdk`).
- Output in `site/`.
- API reference from docstrings.
- Top-level pages: Getting Started, Authentication, Pagination, Error Handling, Extensible Attributes, Migration from `infoblox-client`, then per-domain reference.
- `CLAUDE.md` at repo root mirroring `ibx-uddi-sdk` style: Commands, Architecture, Key Patterns, Code Style, Environment Variables, Testing, Gotchas.

## CI

- GitHub Actions matrix on Python 3.11 / 3.12 / 3.13.
- Jobs: `ruff check`, `ruff format --check`, `mypy`, `pytest` (unit only).
- Integration tests do **not** run in CI (no shared lab Grid). Release checklist item instead.

## Implementation Phasing

### Phase 0 - Project scaffold

- `pyproject.toml`, `src/ibx_nios_sdk/` skeleton, `CLAUDE.md`, `README.md`, CI workflow, ruff/mypy config.
- Empty `NiosClient` that imports cleanly.
- **Gate:** `pip install -e ".[dev]"` works, `pytest` exits 0 with no tests, `mypy` and `ruff` pass.

### Phase 1 - HTTP core (foundation)

- `_http.py`: session login/logout, cookie jar, basic-auth mode, TLS handling, retry, `_return_fields` injection, error classification.
- `_exceptions.py`: full hierarchy.
- `_resource.py`: `WapiResource` base with the full method set.
- `_paging.py`: `AsyncPageIterator`.
- `_common/models.py`: `ExtAttr`, `ExtAttrValue`, shared enums.
- Comprehensive `MockTransport` tests.
- **Gate:** Phase 1 unit tests cover pagination, `_ref` validation, auth-retry (401 → re-login → retry), TLS error wrapping, retry backoff on 429/5xx, `_return_fields` injection, `call_function` with and without `ref`, query-operator kwarg translation. No domain work proceeds until this gate passes.

### Phase 2 - Pilot domain: DNS

- All DNS object types: `zone_auth`, `zone_forward`, `zone_delegated`, `zone_stub`, `zone_rp`, `record:a`, `record:aaaa`, `record:cname`, `record:mx`, `record:txt`, `record:ptr`, `record:srv`, `record:ns`, `record:host`, `record:host_ipv4addr`, `record:host_ipv6addr`, `view`, `nsgroup`, `allrecords`.
- Full models + resources + tests per object.
- `examples/` for DNS workflows.
- DNS docs page drafted.
- **Gate:** review the DNS shape before replicating across the other 16 domains. Pattern bugs caught here don't multiply.

### Phase 3 - Core trio: IPAM + DHCP + Grid

- Three domains, in parallel once Phase 2 is signed off.
- `ipam`: `network`, `networkcontainer`, `range`, `fixedaddress`, `ipv6network`, plus `next_available_ip` / `next_available_network` typed wrappers.
- `dhcp`: option space, option definition, filter, MAC filter, etc.
- `grid`: grid, member, service control, license, license pool, upgrade, HSM, grid DNS/DHCP config objects.
- Integration tests against a lab Grid begin here.

### Phase 4 - Security cluster

- `rpz`, `threatprotection`, `threatinsight`, `security`, `acl`. Five smaller domains as one batch.

### Phase 5 - Everything else

- `dtc`, `cloud`, `discovery`, `federatedrealms`, `microsoftserver`, `smartfolder`, `notification`, `misc`.
- `fileop` inside `misc` is the most irregular; may warrant a mini-spec before implementation.

### Phase 6 - Release hardening

- Zensical site build.
- PyPI 0.1.0 release.
- "Migration from `infoblox-client`" guide.
- Final integration pass against a Grid 9.0.x running WAPI v2.14.

## Open Risks

- **Swagger drift.** Infoblox swaggers are known to lag real WAPI behavior. Budget rework time per domain and record deltas in each `NOTES.md`.
- **Object-count estimate (~300) is a floor.** `grid` and `dns` may surface additional sub-object types during implementation.
- **`fileop` multi-step uploads** will likely need their own design mini-spec when Phase 5 reaches `misc`.
- **Integration-test Grid.** Phase 3 onward depends on access to a lab NIOS Grid. Without one we ship on unit tests + swagger alone and accept higher post-release churn.
