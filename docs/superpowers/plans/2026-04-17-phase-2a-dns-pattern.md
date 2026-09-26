# ibx-nios-sdk Phase 2a: DNS Pattern-Proving Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Stand up the `dns` package, wire it into `NiosClient`, and implement 3 representative DNS resources (`view`, `zone_auth`, `record:a`) end-to-end. This establishes the per-domain pattern every remaining domain will follow.

**Non-goal:** The other 49 DNS object types. Those are Phase 2b (separate plan), expected to be mechanical replication once this pattern is approved.

**Why these 3 exemplars:**
- `view` - simple, few fields (86 props but mostly optional scalars), exercises the basic CRUD + `find_one` flow.
- `zone_auth` - 129 props, most complex DNS object, heavy nested types (shared enums for grid/primaries), exercises the shared-models split.
- `record:a` - 25 props, canonical "record type" shape that all other `record:*` types follow by mechanical replication.

**Tech Stack:** Python 3.11+, `httpx>=0.27`, `pydantic>=2`. Foundation from Phase 0+1 (NiosClient, HttpClient, WapiResource) is assumed and must not be modified in this plan.

**Spec reference:** `docs/superpowers/specs/2026-04-17-ibx-nios-sdk-design.md` §4 (Models).

---

## File Structure (end state of this plan)

```
schemas/v2.14/dns.json                              # committed snapshot

src/ibx_nios_sdk/
├── client.py                                       # MODIFIED: add `dns` cached_property
└── dns/
    ├── __init__.py                                 # re-exports: DnsService, ViewResource, ZoneAuthResource, RecordAResource
    ├── _service.py                                 # DnsService with @cached_property per resource
    ├── _view.py                                    # ViewResource
    ├── _zone_auth.py                               # ZoneAuthResource
    ├── _record_a.py                                # RecordAResource
    ├── NOTES.md                                    # swagger-vs-reality deltas (seed)
    └── models/
        ├── __init__.py                             # re-exports: View, ZoneAuth, RecordA + shared types
        ├── _shared.py                              # cross-resource nested types (ExtServer, GridPrimary enums, etc.)
        ├── view.py                                 # View pydantic model
        ├── zone_auth.py                            # ZoneAuth pydantic model + nested types it owns
        └── record_a.py                             # RecordA pydantic model + RecordACloudInfo etc.

tests/
├── test_client.py                                  # MODIFIED: assert `client.dns` returns DnsService
└── dns/
    ├── __init__.py                                 # empty
    ├── conftest.py                                 # dns-specific test helpers
    ├── test_service.py
    ├── test_view.py
    ├── test_zone_auth.py
    └── test_record_a.py
```

---

## Task 1: Download and commit the DNS swagger snapshot

**Files:**
- Create: `schemas/v2.14/dns.json`

- [ ] **Step 1.1: Download snapshot**

```bash
cd /Users/mjsmith/dev-projects/ibx-nios-sdk
curl -fsSL -o schemas/v2.14/dns.json \
  https://infobloxopen.github.io/nios-swagger/swagger-ui/openspec/v2.14/dns.json
```

Expected: file is ~1 MB of JSON. Verify with `python3 -c "import json; d=json.load(open('schemas/v2.14/dns.json')); print(d['info']['version'], len(d['paths']))"` → `2.14 119`.

- [ ] **Step 1.2: Commit**

```bash
git add schemas/v2.14/dns.json
git commit -m "chore: snapshot NIOS WAPI v2.14 DNS swagger"
```

---

## Task 2: `dns/` package skeleton + wire `DnsService` into `NiosClient`

**Files:**
- Create: `src/ibx_nios_sdk/dns/__init__.py`
- Create: `src/ibx_nios_sdk/dns/_service.py`
- Create: `src/ibx_nios_sdk/dns/NOTES.md`
- Create: `src/ibx_nios_sdk/dns/models/__init__.py`
- Modify: `src/ibx_nios_sdk/client.py`
- Modify: `src/ibx_nios_sdk/__init__.py`
- Create: `tests/dns/__init__.py`
- Create: `tests/dns/conftest.py`
- Create: `tests/dns/test_service.py`
- Modify: `tests/test_client.py`

- [ ] **Step 2.1: Write failing service/client tests**

`tests/dns/__init__.py` - empty.

`tests/dns/conftest.py`:

```python
"""DNS-specific test helpers."""

from __future__ import annotations

import httpx

from tests.conftest import json_response


def dns_session_handler_factory(path_response_map):
    """Build a MockTransport handler that logs in, then routes by path to the
    (status, body) pair provided in ``path_response_map``.

    path_response_map: dict[str, tuple[int, Any]] - path -> (status_code, body)
    """
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls.append(request)
        for path, (status, body) in path_response_map.items():
            if path in request.url.path:
                return json_response(body, status_code=status)
        return json_response({"Error": "no handler", "text": request.url.path}, status_code=404)

    return handler, calls
```

`tests/dns/test_service.py`:

```python
"""DnsService wiring: cached_property per resource, shares the HttpClient."""

from __future__ import annotations

import httpx

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns import DnsService, RecordAResource, ViewResource, ZoneAuthResource


def test_dns_service_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    svc1 = client.dns
    svc2 = client.dns
    assert svc1 is svc2, "client.dns must be cached"
    assert isinstance(svc1, DnsService)


def test_dns_resources_cached_property() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )

    dns = client.dns
    assert isinstance(dns.view, ViewResource)
    assert isinstance(dns.zone_auth, ZoneAuthResource)
    assert isinstance(dns.record_a, RecordAResource)

    # caching
    assert dns.view is dns.view
    assert dns.zone_auth is dns.zone_auth
    assert dns.record_a is dns.record_a
```

Append to `tests/test_client.py` (at the end of the file):

```python
async def test_nios_client_dns_service() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    from ibx_nios_sdk.dns import DnsService

    transport = httpx.MockTransport(handler)
    client = NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=transport,
    )
    try:
        assert isinstance(client.dns, DnsService)
    finally:
        await client.aclose()
```

- [ ] **Step 2.2: Run - all new tests FAIL**

```bash
pytest tests/dns/ tests/test_client.py::test_nios_client_dns_service -v
```

Expected: ImportError on `ibx_nios_sdk.dns`.

- [ ] **Step 2.3: Implement `src/ibx_nios_sdk/dns/models/__init__.py`** (stub for now)

```python
"""DNS domain pydantic models."""

from __future__ import annotations

__all__: list[str] = []
```

- [ ] **Step 2.4: Implement `src/ibx_nios_sdk/dns/NOTES.md`**

```markdown
# DNS domain - swagger-vs-reality notes

Record any places where the NIOS v2.14 WAPI behavior diverges from
`schemas/v2.14/dns.json`. Each entry should include:

- Object and field affected
- What the swagger claims
- What WAPI actually does
- Workaround in the SDK (e.g. model override, readonly strip, etc.)

_(Seed file - populated as issues are discovered during implementation.)_
```

- [ ] **Step 2.5: Implement `src/ibx_nios_sdk/dns/_service.py`**

```python
"""DnsService - entry point for DNS resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.dns._record_a import RecordAResource
    from ibx_nios_sdk.dns._view import ViewResource
    from ibx_nios_sdk.dns._zone_auth import ZoneAuthResource


class DnsService:
    """Entry point for NIOS DNS resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    @cached_property
    def view(self) -> ViewResource:
        from ibx_nios_sdk.dns._view import ViewResource

        return ViewResource(self._client)

    @cached_property
    def zone_auth(self) -> ZoneAuthResource:
        from ibx_nios_sdk.dns._zone_auth import ZoneAuthResource

        return ZoneAuthResource(self._client)

    @cached_property
    def record_a(self) -> RecordAResource:
        from ibx_nios_sdk.dns._record_a import RecordAResource

        return RecordAResource(self._client)
```

- [ ] **Step 2.6: Placeholder resource files** (will be fully implemented in Tasks 4–6)

`src/ibx_nios_sdk/dns/_view.py`:

```python
"""View resource - placeholder, fully implemented in Task 4."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.view import View


class ViewResource(WapiResource[View]):
    _wapi_type = "view"
    _model = View
    _default_return_fields = ["name", "is_default", "comment"]
```

`src/ibx_nios_sdk/dns/_zone_auth.py`:

```python
"""ZoneAuth resource - placeholder, fully implemented in Task 5."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_auth import ZoneAuth


class ZoneAuthResource(WapiResource[ZoneAuth]):
    _wapi_type = "zone_auth"
    _model = ZoneAuth
    _default_return_fields = ["fqdn", "view", "comment"]
```

`src/ibx_nios_sdk/dns/_record_a.py`:

```python
"""RecordA resource - placeholder, fully implemented in Task 6."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_a import RecordA


class RecordAResource(WapiResource[RecordA]):
    _wapi_type = "record:a"
    _model = RecordA
    _default_return_fields = ["name", "ipv4addr", "view"]
```

- [ ] **Step 2.7: Create minimal model stubs** (will be expanded in Tasks 4–6)

`src/ibx_nios_sdk/dns/models/view.py`:

```python
"""View pydantic model - stub, expanded in Task 4."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class View(BaseModel):
    """Stub; full field set populated in Task 4."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = None
    name: str | None = None
```

`src/ibx_nios_sdk/dns/models/zone_auth.py`:

```python
"""ZoneAuth pydantic model - stub, expanded in Task 5."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ZoneAuth(BaseModel):
    """Stub; full field set populated in Task 5."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = None
    fqdn: str | None = None
```

`src/ibx_nios_sdk/dns/models/record_a.py`:

```python
"""RecordA pydantic model - stub, expanded in Task 6."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RecordA(BaseModel):
    """Stub; full field set populated in Task 6."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = None
    name: str | None = None
```

- [ ] **Step 2.8: Implement `src/ibx_nios_sdk/dns/__init__.py`**

```python
"""DNS domain - NIOS DNS objects (zones, records, views, nsgroups)."""

from __future__ import annotations

from ibx_nios_sdk.dns._record_a import RecordAResource
from ibx_nios_sdk.dns._service import DnsService
from ibx_nios_sdk.dns._view import ViewResource
from ibx_nios_sdk.dns._zone_auth import ZoneAuthResource

__all__ = [
    "DnsService",
    "RecordAResource",
    "ViewResource",
    "ZoneAuthResource",
]
```

- [ ] **Step 2.9: Wire `DnsService` into `NiosClient`**

Modify `src/ibx_nios_sdk/client.py`:

Add these imports to the top (under existing imports, inside `TYPE_CHECKING` block if you create one, or as normal imports):

```python
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ibx_nios_sdk.dns import DnsService
```

Add this cached_property inside `NiosClient`, after the `grid_url` property:

```python
    @cached_property
    def dns(self) -> DnsService:
        from ibx_nios_sdk.dns import DnsService

        return DnsService(self._http)
```

(Use a runtime-local import inside the property to keep the top-of-module import graph DAG-shaped and avoid import-time circulars.)

- [ ] **Step 2.10: Update `src/ibx_nios_sdk/__init__.py` to re-export DnsService**

Add `from ibx_nios_sdk.dns import DnsService` and add `"DnsService"` to `__all__`. Keep everything else as-is.

- [ ] **Step 2.11: Run tests - all pass**

```bash
pytest -v
mypy
ruff check src/ tests/
ruff format --check src/ tests/
```

Expected: 66 prior tests + 3 new tests = 69 PASSED; mypy/ruff clean.

- [ ] **Step 2.12: Commit**

```bash
git add src/ibx_nios_sdk/dns/ src/ibx_nios_sdk/client.py src/ibx_nios_sdk/__init__.py tests/dns/ tests/test_client.py
git commit -m "feat(dns): scaffold dns package and wire DnsService into NiosClient"
```

---

## Task 3: DNS shared models (`dns/models/_shared.py`)

**Purpose:** Seed the domain-local shared types that `View`, `ZoneAuth`, `RecordA` will all reference (grid primary / external server / discovered-data blocks). Start with only the pieces the three exemplars actually need; grow organically for other resources later.

**Files:**
- Create: `src/ibx_nios_sdk/dns/models/_shared.py`
- Create: `tests/dns/test_shared_models.py`

- [ ] **Step 3.1: Consult the swagger** for the shapes of these nested types. Read `schemas/v2.14/dns.json`, find the schemas under `components.schemas`:
    - `ExtServer` - used by `ZoneAuth.grid_primary` list and `RecordA.aws_rte53_record_info`
    - `MemberServer` - used by `ZoneAuth.grid_primary`
    - `RecordACloudInfo` / `ZoneAuthCloudInfo` / `ViewCloudInfo` - same shape; a shared `CloudInfo` is fine.
    - `RecordADiscoveredData` - used by `RecordA`
    - `RecordAMsAdUserData` - used by `RecordA`

Field lists and types are in the swagger. Copy exact field names and types; preserve `readOnly` markers via a `_SHARED_READONLY_FIELDS: frozenset[str]` set at module level if needed, though for nested types readOnly mostly doesn't matter (nested models are not the update target).

- [ ] **Step 3.2: Write failing tests**

`tests/dns/test_shared_models.py`:

```python
"""Tests for DNS shared nested-type models."""

from __future__ import annotations

from ibx_nios_sdk.dns.models._shared import (
    CloudInfo,
    ExtServer,
    MemberServer,
)


def test_ext_server_parses_minimal_payload() -> None:
    ext = ExtServer.model_validate({"address": "10.0.0.1", "name": "dns1.example.com"})
    assert ext.address == "10.0.0.1"
    assert ext.name == "dns1.example.com"


def test_ext_server_supports_stealth_and_tsig() -> None:
    ext = ExtServer.model_validate({
        "address": "10.0.0.1",
        "name": "dns1.example.com",
        "stealth": True,
        "tsig_key_name": "my-key",
        "tsig_key_alg": "HMAC-SHA256",
        "use_tsig_key_name": True,
    })
    assert ext.stealth is True
    assert ext.tsig_key_alg == "HMAC-SHA256"


def test_member_server_parses() -> None:
    ms = MemberServer.model_validate({
        "name": "member1.local",
        "enable_preferred_primaries": False,
        "grid_replicate": True,
        "lead": False,
        "stealth": False,
    })
    assert ms.name == "member1.local"
    assert ms.grid_replicate is True


def test_cloud_info_parses() -> None:
    ci = CloudInfo.model_validate({
        "authority_type": "GM",
        "delegated_scope": "ROOT",
    })
    assert ci.authority_type == "GM"


def test_extra_fields_allowed() -> None:
    ext = ExtServer.model_validate({"address": "1.1.1.1", "name": "x", "some_new_field": 123})
    assert ext.address == "1.1.1.1"
```

- [ ] **Step 3.3: Run tests - FAIL on import**

- [ ] **Step 3.4: Implement `src/ibx_nios_sdk/dns/models/_shared.py`**

Use the swagger schemas for `ExtServer`, `MemberServer`, and the common `*CloudInfo` shapes (pick the superset of fields across the three - they largely overlap).

Template (verify each field against the swagger; fill in fields not shown here by following the same pattern):

```python
"""Shared nested-type models used across DNS resources."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class _DnsNested(BaseModel):
    """Base for DNS nested types: permissive, name-aware, no-_ref."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ExtServer(_DnsNested):
    """External DNS server reference - used by grid_primary, forwarders, etc."""

    address: str | None = None
    name: str | None = None
    stealth: bool | None = None
    tsig_key: str | None = None
    tsig_key_alg: str | None = None
    tsig_key_name: str | None = None
    use_tsig_key_name: bool | None = None
    shared_with_ms_parent_delegation: bool | None = None


class MemberServer(_DnsNested):
    """NIOS Grid member acting as a DNS server."""

    name: str | None = None
    enable_preferred_primaries: bool | None = None
    grid_replicate: bool | None = None
    lead: bool | None = None
    preferred_primaries: list[ExtServer] | None = None
    stealth: bool | None = None


class CloudInfo(_DnsNested):
    """Cloud provider / delegation metadata common to most DNS objects."""

    authority_type: str | None = None
    delegated_member: Any | None = None
    delegated_root: str | None = None
    delegated_scope: str | None = None
    mgmt_platform: str | None = None
    owned_by_adapter: bool | None = None
    tenant: str | None = None
    usage: str | None = None
```

Consult the swagger for any additional fields. If any field name collides with a Python keyword, use a trailing underscore + `Field(alias="view")` pattern (unlikely for these specific types).

- [ ] **Step 3.5: Run tests + tooling - all pass**

- [ ] **Step 3.6: Commit**

```bash
git add src/ibx_nios_sdk/dns/models/_shared.py tests/dns/test_shared_models.py
git commit -m "feat(dns): add shared nested models (ExtServer, MemberServer, CloudInfo)"
```

---

## Task 4: `View` model + `ViewResource` - full implementation

**Pattern-proving task.** `view` is the simplest of the three exemplars: top-level DNS object, ~86 props, no nested records. The full-field model + resource + tests you produce here is the template that every other Phase 2b resource follows.

**Files:**
- Modify: `src/ibx_nios_sdk/dns/models/view.py` (replace stub with full model)
- Modify: `src/ibx_nios_sdk/dns/_view.py` (replace stub)
- Modify: `src/ibx_nios_sdk/dns/models/__init__.py` (export `View`)
- Create: `tests/dns/test_view.py`

- [ ] **Step 4.1: Consult the swagger** - read `schemas/v2.14/dns.json`, schema `View`. List every property with its type and `readOnly` flag.

- [ ] **Step 4.2: Write failing tests**

`tests/dns/test_view.py`:

```python
"""ViewResource - CRUD, find_one, list, pagination."""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk.dns.models.view import View
from tests.conftest import json_response


def _client(handler) -> NiosClient:
    return NiosClient(
        grid_url="https://g.example.com",
        username="admin",
        password="x",
        _transport=httpx.MockTransport(handler),
    )


async def test_view_list_default_view() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({
            "result": [
                {"_ref": "view/ZG5zLnZpZXck:default/true", "name": "default", "is_default": True, "comment": ""}
            ],
            "next_page_id": "",
        })

    async with _client(handler) as c:
        views = await c.dns.view.list().all()
        assert len(views) == 1
        v = views[0]
        assert v.name == "default"
        assert v.is_default is True

        # verify WAPI params
        params = captured[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert "name" in params["_return_fields+"]


async def test_view_get_by_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({
            "_ref": "view/ABC:custom/false",
            "name": "custom",
            "is_default": False,
            "comment": "test view",
        })

    async with _client(handler) as c:
        ref = "view/ABC:custom/false"
        v = await c.dns.view.get(ref)
        assert v.name == "custom"
        assert v.comment == "test view"


async def test_view_find_one() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response({
            "result": [{"_ref": "view/X:custom/false", "name": "custom", "is_default": False}],
            "next_page_id": "",
        })

    async with _client(handler) as c:
        v = await c.dns.view.find_one(name="custom")
        assert v is not None
        assert v.name == "custom"


async def test_view_create() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "view/NEW:custom/false", "name": "custom", "is_default": False})

    async with _client(handler) as c:
        v = await c.dns.view.create({"name": "custom", "comment": "new view"})
        assert v.name == "custom"
        body = captured[0].content.decode()
        assert '"name":"custom"' in body
        assert '"comment":"new view"' in body


async def test_view_update_strips_readonly() -> None:
    """is_default is read-only in the swagger; it must not be PUT."""
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        captured.append(request)
        return json_response({"_ref": "view/ABC:custom/false", "name": "custom2"})

    async with _client(handler) as c:
        ref = "view/ABC:custom/false"
        v = View(name="custom2", is_default=True, comment="renamed")
        await c.dns.view.update(ref, v)
        body = captured[0].content.decode()
        assert '"is_default"' not in body, "readonly field must be stripped from update body"
        assert '"name":"custom2"' in body


async def test_view_delete() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})
        return json_response("view/ABC:custom/false")

    async with _client(handler) as c:
        result = await c.dns.view.delete("view/ABC:custom/false")
        assert result == "view/ABC:custom/false"
```

- [ ] **Step 4.3: Run - tests FAIL**

- [ ] **Step 4.4: Implement `src/ibx_nios_sdk/dns/models/view.py` - full model**

Replace the stub with the full model. Approach:
1. Open `schemas/v2.14/dns.json`, find `components.schemas.View`.
2. For every property, create a `field_name: <type> | None = None` entry (all fields optional on create, NIOS validates server-side).
3. Mark `readOnly: true` fields as RO and collect them into a module-level `READONLY_FIELDS` set - exported so the resource can register them.
4. Map types: `string` → `str`, `integer` → `int`, `boolean` → `bool`, `object` → `dict[str, Any]`, `array` → `list[...]`, `$ref` → typed reference to the nested class. For fields referring to shared nested types (`ExtServer`, `MemberServer`, `CloudInfo`), import from `_shared.py`.
5. Keyword collisions: `view` → `view_` aliased; `type` → `type_` aliased. Python 3.11+ so no `class` collision worry (rare in NIOS data anyway).

Skeleton:

```python
"""View - NIOS DNS view (resolution/query segmentation)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk.dns.models._shared import CloudInfo, ExtServer


READONLY_FIELDS: frozenset[str] = frozenset({
    "cloud_info",
    "is_default",
    "ms_ad_user_data",
    # ...populate from swagger readOnly=true fields
})


class View(BaseModel):
    """NIOS DNS view configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref")
    name: str | None = None
    comment: str | None = None
    is_default: bool | None = None
    disable: bool | None = None

    # ... full field set from swagger View schema, ~86 fields total
    cloud_info: CloudInfo | None = None
    forwarders: list[ExtServer] | None = None

    # Add all remaining fields from the swagger. Use `| None = None` for every
    # field (WAPI tolerates absent fields on create/update).
```

**Required:** every field from the swagger must appear on the model. You may omit deep nested fields (e.g., `dnssec_ksk_rollover_notification_config`) by typing them as `dict[str, Any] | None` for now - note them in `dns/NOTES.md`.

- [ ] **Step 4.5: Implement `src/ibx_nios_sdk/dns/_view.py`** - full resource

```python
"""View resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.view import READONLY_FIELDS, View


class ViewResource(WapiResource[View]):
    _wapi_type = "view"
    _model = View
    _default_return_fields = ["name", "is_default", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
```

`_default_return_fields` should be a conservative "identity + human-readable" subset (5–10 fields). The full model populates when users request `return_fields_plus=["cloud_info", "forwarders", ...]`.

- [ ] **Step 4.6: Export `View` from `dns/models/__init__.py`**

```python
"""DNS domain pydantic models."""

from __future__ import annotations

from ibx_nios_sdk.dns.models.view import View

__all__ = ["View"]
```

- [ ] **Step 4.7: Run all tests + tooling**

```bash
pytest tests/dns/ -v
pytest -v            # full suite
mypy
ruff check src/ tests/
ruff format --check src/ tests/
```

All clean.

- [ ] **Step 4.8: Commit**

```bash
git add src/ibx_nios_sdk/dns/models/view.py src/ibx_nios_sdk/dns/models/__init__.py \
        src/ibx_nios_sdk/dns/_view.py tests/dns/test_view.py
git commit -m "feat(dns): full View model and ViewResource"
```

---

## Task 5: `ZoneAuth` model + `ZoneAuthResource` - most complex exemplar

**Pattern-proving for complex zones.** `zone_auth` has 129 props, the largest of any DNS object. It exercises:
- Lists of nested types (`grid_primary`, `grid_secondaries`, `external_primaries`, `external_secondaries`)
- Enum-valued strings (zone format, signing algorithm, etc.)
- Read-only fields galore
- Function calls (`copyzonerecords`, `restartifneeded`, `lock_unlock_zone`)

**Files:**
- Modify: `src/ibx_nios_sdk/dns/models/zone_auth.py`
- Modify: `src/ibx_nios_sdk/dns/_zone_auth.py`
- Modify: `src/ibx_nios_sdk/dns/models/__init__.py` (export)
- Create: `tests/dns/test_zone_auth.py`

- [ ] **Step 5.1: Consult swagger** - `components.schemas.ZoneAuth`. Note the field count; populate everything.

- [ ] **Step 5.2: Write failing tests** - mirror `test_view.py` structure, plus one function-call test:

`tests/dns/test_zone_auth.py` - include tests for:

1. `list(view="default")` populates the `view` filter and returns parsed `ZoneAuth` instances.
2. `get(ref)` returns a `ZoneAuth` with `fqdn`, `view`, `zone_format`, and a non-empty `grid_primary` list.
3. `find_one(fqdn="example.com")`.
4. `create({"fqdn": "example.com", "view": "default", "grid_primary": [{"name": "member1"}]})` - verify the POST body includes nested grid_primary correctly.
5. `update(ref, {"comment": "new"})` - verify PUT uses the ref.
6. `delete(ref)` returns the ref.
7. `call_function(ref, "copyzonerecords", zone="src.example.com", view="default")` - verify POST with `?_function=copyzonerecords`.
8. Read-only fields (e.g., `soa_default_ttl`, `last_queried`, `dnssec_key_params`) are stripped from update bodies.

Each test follows the pattern from `test_view.py` - handler captures, assertion against `req.url.params` / `req.content`.

- [ ] **Step 5.3: Run - FAIL**

- [ ] **Step 5.4: Implement full `ZoneAuth` model**

Approach is identical to Task 4.4: read swagger, create `name: type | None = None` for each property, mark readOnly fields, use `_shared.py` types for `grid_primary`/etc.

Where the swagger uses `$ref` to nested types that are specific to `ZoneAuth` (and not used elsewhere), define them inline in `zone_auth.py`:

```python
class ZoneAuthGridPrimary(_DnsNested):
    """member entry in ZoneAuth.grid_primary list."""
    name: str | None = None
    stealth: bool | None = None
    grid_replicate: bool | None = None
    lead: bool | None = None
    preferred_primaries: list[ExtServer] | None = None
    enable_preferred_primaries: bool | None = None

# ZoneAuth-specific nested types like ZoneAuthDnssecKeyParams, etc.
# Use dict[str, Any] for deeply nested or rarely-used fields and add a NOTES.md entry.
```

Import `_DnsNested` from `_shared.py` - or duplicate the pattern; we'll consolidate if it becomes repetitive across resources.

Full field set required. Update `READONLY_FIELDS` to match the swagger's `readOnly: true` markers.

- [ ] **Step 5.5: Implement full `ZoneAuthResource`**

```python
"""ZoneAuth resource with typed function wrappers."""

from __future__ import annotations

from typing import Any

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_auth import READONLY_FIELDS, ZoneAuth


class ZoneAuthResource(WapiResource[ZoneAuth]):
    _wapi_type = "zone_auth"
    _model = ZoneAuth
    _default_return_fields = ["fqdn", "view", "comment", "zone_format", "disable"]
    _readonly_fields = set(READONLY_FIELDS)

    async def copy_zone_records(
        self,
        ref: str,
        *,
        source_zone: str,
        view: str | None = None,
        copy_all_records: bool | None = None,
    ) -> dict[str, Any]:
        """WAPI function: copyzonerecords - copy records from another zone."""
        kwargs: dict[str, Any] = {"zone": source_zone}
        if view is not None:
            kwargs["view"] = view
        if copy_all_records is not None:
            kwargs["copy_all_records"] = copy_all_records
        return await self.call_function(ref, "copyzonerecords", **kwargs)

    async def lock_unlock_zone(self, ref: str, *, lock: bool) -> dict[str, Any]:
        return await self.call_function(ref, "lock_unlock_zone", operation="LOCK" if lock else "UNLOCK")
```

Only add the most common typed wrappers - the rest stay accessible via `call_function(ref, "function_name", ...)`.

- [ ] **Step 5.6: Run tests + tooling - all clean**

- [ ] **Step 5.7: Commit**

```bash
git add src/ibx_nios_sdk/dns/models/zone_auth.py src/ibx_nios_sdk/dns/models/__init__.py \
        src/ibx_nios_sdk/dns/_zone_auth.py tests/dns/test_zone_auth.py
git commit -m "feat(dns): full ZoneAuth model, resource, and typed function wrappers"
```

---

## Task 6: `RecordA` model + `RecordAResource` - canonical record pattern

**Pattern-proving for record types.** Every `record:*` in DNS follows this shape (25-ish fields, `name`/`ipv4addr` or `name`/`ipv6addr` key fields, cloud/discovered/ms_ad metadata). The code you write here will be the template for the 23 remaining record types.

**Files:**
- Modify: `src/ibx_nios_sdk/dns/models/record_a.py`
- Modify: `src/ibx_nios_sdk/dns/_record_a.py`
- Modify: `src/ibx_nios_sdk/dns/models/__init__.py`
- Create: `tests/dns/test_record_a.py`

- [ ] **Step 6.1: Consult swagger** - `components.schemas.RecordA`. Note nested types `RecordACloudInfo`, `RecordADiscoveredData`, `RecordAMsAdUserData`, `RecordAAwsRte53RecordInfo` - these can reuse the shared `CloudInfo` where field sets match; others live inline in `record_a.py`.

- [ ] **Step 6.2: Write failing tests**

`tests/dns/test_record_a.py` - include tests for:
1. `list(zone="example.com")` with WAPI filter translation.
2. `list(name__like="host")` → `name~=host` query param.
3. `get(ref)` returns parsed model with `name`, `ipv4addr`, `view`, `comment`.
4. `find_one(name="host.example.com")`.
5. `create({"name": "...", "ipv4addr": "..."})`.
6. `update(ref, {"comment": "..."})`.
7. `delete(ref)` returns ref.
8. `extattrs` round-trip: list → parse `extattrs` as `dict[str, ExtAttrValue]`.
9. `set_extattrs(ref, Site="NYC")` → PUT with correctly-shaped `extattrs` body.
10. Readonly fields (`creation_time`, `last_queried`, `dns_name`, `reclaimable`, `shared_record_group`) stripped from update body.

Each assertion follows the `test_view.py` pattern.

- [ ] **Step 6.3: Run - FAIL**

- [ ] **Step 6.4: Implement full `RecordA` model**

```python
"""RecordA - DNS A record (name → IPv4 mapping)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.dns.models._shared import CloudInfo, _DnsNested


READONLY_FIELDS: frozenset[str] = frozenset({
    "creation_time",
    "creator",
    "dns_name",
    "last_queried",
    "reclaimable",
    "shared_record_group",
    "ms_ad_user_data",
    # add the rest per the swagger's readOnly markers
})


class RecordADiscoveredData(_DnsNested):
    """Discovery-plugin metadata attached to a RecordA."""
    bgp_as: int | None = None
    bridge_domain: str | None = None
    # ...add every field from swagger RecordADiscoveredData


class RecordAMsAdUserData(_DnsNested):
    """Microsoft AD-integrated record metadata."""
    active_users_count: int | None = None


class RecordAAwsRte53RecordInfo(_DnsNested):
    """AWS Route53 shadow record metadata."""
    alias_target_dns_name: str | None = None
    alias_target_hosted_zone_id: str | None = None
    alias_target_evaluate_target_health: bool | None = None
    failover: str | None = None
    geo_location: dict[str, Any] | None = None
    health_check_id: str | None = None
    region: str | None = None
    set_identifier: str | None = None
    type_: str | None = Field(default=None, alias="type")
    weight: int | None = None


class RecordA(BaseModel):
    """DNS A record."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref")
    name: str | None = None
    ipv4addr: str | None = None  # swagger declares ipv4addr without a type - string per WAPI docs
    view_: str | None = Field(default=None, alias="view")
    zone: str | None = None
    comment: str | None = None
    creation_time: int | None = None
    creator: str | None = None
    ddns_principal: str | None = None
    ddns_protected: bool | None = None
    disable: bool | None = None
    discovered_data: RecordADiscoveredData | None = None
    dns_name: str | None = None
    extattrs: dict[str, ExtAttrValue] | None = None
    forbid_reclamation: bool | None = None
    last_queried: int | None = None
    ms_ad_user_data: RecordAMsAdUserData | None = None
    reclaimable: bool | None = None
    remove_associated_ptr: bool | None = None
    shared_record_group: str | None = None
    aws_rte53_record_info: RecordAAwsRte53RecordInfo | None = None
    cloud_info: CloudInfo | None = None
    # ...all 25 fields from the swagger
```

- [ ] **Step 6.5: Implement full `RecordAResource`**

```python
"""RecordA resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_a import READONLY_FIELDS, RecordA


class RecordAResource(WapiResource[RecordA]):
    _wapi_type = "record:a"
    _model = RecordA
    _default_return_fields = [
        "name", "ipv4addr", "view", "zone", "comment", "disable",
    ]
    _readonly_fields = set(READONLY_FIELDS)
```

No typed function wrappers yet - `record:a` has no standard WAPI functions. If one is added in a future WAPI version, expose it here.

- [ ] **Step 6.6: Export from `dns/models/__init__.py`**

```python
from ibx_nios_sdk.dns.models.record_a import RecordA
from ibx_nios_sdk.dns.models.view import View
from ibx_nios_sdk.dns.models.zone_auth import ZoneAuth

__all__ = ["RecordA", "View", "ZoneAuth"]
```

- [ ] **Step 6.7: Run full suite + tooling**

```bash
pytest -v
mypy
ruff check src/ tests/
ruff format --check src/ tests/
```

All clean.

- [ ] **Step 6.8: Commit**

```bash
git add src/ibx_nios_sdk/dns/models/record_a.py src/ibx_nios_sdk/dns/models/__init__.py \
        src/ibx_nios_sdk/dns/_record_a.py tests/dns/test_record_a.py
git commit -m "feat(dns): full RecordA model and RecordAResource"
```

---

## Task 7: End-to-end example + NOTES.md pattern documentation

**Files:**
- Create: `examples/01_create_a_record.py`
- Create: `examples/02_list_zones.py`
- Modify: `src/ibx_nios_sdk/dns/NOTES.md` (document the pattern used in Tasks 4–6)

- [ ] **Step 7.1: Write `examples/01_create_a_record.py`**

```python
"""Create a DNS A record.

Env vars required:
    NIOS_GRID_URL, NIOS_USERNAME, NIOS_PASSWORD
"""

from __future__ import annotations

import asyncio

from ibx_nios_sdk import NiosClient


async def main() -> None:
    async with NiosClient() as client:
        # Ensure the zone exists
        zone = await client.dns.zone_auth.find_one(fqdn="example.com")
        if zone is None:
            print("zone example.com not found; create it first")
            return

        # Create an A record
        created = await client.dns.record_a.create({
            "name": "host.example.com",
            "ipv4addr": "10.0.0.42",
            "view": zone.view_ or "default",
            "comment": "created by ibx-nios-sdk example",
        })
        print("created:", created.ref)


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 7.2: Write `examples/02_list_zones.py`**

```python
"""List authoritative zones and their A-record counts."""

from __future__ import annotations

import asyncio

from ibx_nios_sdk import NiosClient


async def main() -> None:
    async with NiosClient() as client:
        async for zone in client.dns.zone_auth.list():
            records = await client.dns.record_a.list(zone=zone.fqdn).all()
            print(f"{zone.fqdn:40s} view={zone.view_:15s} A-records={len(records)}")


if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] **Step 7.3: Expand `src/ibx_nios_sdk/dns/NOTES.md` with the pattern guide**

```markdown
# DNS domain - swagger-vs-reality notes + resource pattern

## Per-object file layout

For each new WAPI object type ``<wapi:type>``:

1. **Model** → ``src/ibx_nios_sdk/dns/models/<snake_case>.py`` containing:
   - A ``READONLY_FIELDS: frozenset[str]`` of field names the swagger marks
     ``readOnly: true``. These are stripped on PUT.
   - Inline nested-type classes for schemas not reused elsewhere
     (e.g. ``RecordAAwsRte53RecordInfo``).
   - The main BaseModel class with ``ConfigDict(populate_by_name=True, extra="allow")``.
   - ``ref: str | None = Field(default=None, alias="_ref")``.
   - Every field from the swagger, typed as ``<type> | None = None``.
   - Python keyword collisions use trailing underscore + ``Field(alias="...")``.

2. **Resource** → ``src/ibx_nios_sdk/dns/_<snake_case>.py``:
   - Subclass ``WapiResource[<Model>]``.
   - ``_wapi_type`` = exact WAPI type string (e.g. ``"record:a"``).
   - ``_model`` = the pydantic class.
   - ``_default_return_fields`` = 5–10 identity/human-readable fields.
   - ``_readonly_fields`` = ``set(<ModelModule>.READONLY_FIELDS)``.
   - Typed method wrappers ONLY for functions used in >50% of user scripts
     (e.g. ``zone_auth.copy_zone_records``). Others use ``.call_function(ref, ...)``.

3. **Service wiring** → add ``@cached_property`` in ``dns/_service.py``.

4. **Export** from ``dns/__init__.py`` and ``dns/models/__init__.py``.

5. **Tests** → ``tests/dns/test_<snake_case>.py`` covering:
   - list (with representative filter)
   - get by _ref
   - find_one
   - create (body content + _return_as_object param)
   - update (readonly field strip)
   - delete (returns ref)
   - extattrs round-trip (for objects that support extattrs)
   - one function call (if any typed wrappers added)

## Swagger-vs-reality deltas

_(populated as discovered)_
```

- [ ] **Step 7.4: Run final full suite + tooling**

```bash
pytest -v
mypy
ruff check src/ tests/
ruff format --check src/ tests/
python -c "from ibx_nios_sdk import NiosClient; from ibx_nios_sdk.dns import DnsService; print('ok')"
```

All clean.

- [ ] **Step 7.5: Commit**

```bash
git add examples/ src/ibx_nios_sdk/dns/NOTES.md
git commit -m "docs(dns): add examples and resource pattern guide"
```

---

## Verification Checklist

- [ ] `pytest -v` passes (≥75 tests total).
- [ ] `mypy` clean in strict mode.
- [ ] `ruff check` and `ruff format --check` clean.
- [ ] `schemas/v2.14/dns.json` committed and valid JSON.
- [ ] `from ibx_nios_sdk.dns import DnsService, ViewResource, ZoneAuthResource, RecordAResource` works.
- [ ] `client.dns.view`, `client.dns.zone_auth`, `client.dns.record_a` each return correct resource subclass.
- [ ] `client.dns.record_a.list(zone="example.com")` returns an `AsyncPageIterator` yielding `RecordA`.
- [ ] `ZoneAuthResource.copy_zone_records()` typed wrapper exists and POSTs `?_function=copyzonerecords`.
- [ ] `dns/NOTES.md` contains the pattern guide for future phases.

## Out of Scope (Phase 2b and beyond)

- The other 49 DNS object types (all record:* beyond record:a, zone_forward/delegated/stub/rp, nsgroups, shared records, discrepancy objects, dns64group, record name policy, etc.).
- Typed wrappers for less common DNS WAPI functions.
- DNS docs page in Zensical (Phase 6).
- Integration tests against a real Grid.
