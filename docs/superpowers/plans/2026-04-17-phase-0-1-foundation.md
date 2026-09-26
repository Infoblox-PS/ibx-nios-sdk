# ibx-nios-sdk Phase 0+1: Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the `ibx-nios-sdk` repo with a working HTTP/auth/resource foundation that every future WAPI domain will build on.

**Architecture:** Async-only Python 3.11+ SDK. `NiosClient` → per-domain `@cached_property` services → `WapiResource` subclasses → single shared `HttpClient` wrapping `httpx.AsyncClient` at `/wapi/v{version}/`. Session-cookie auth by default, basic-auth opt-in. Auto-paginated `list()`, hand-written pydantic v2 models.

**Tech Stack:** Python 3.11+, `httpx>=0.27`, `pydantic>=2`, `python-dateutil>=2.8.2`, `pytest`, `pytest-asyncio`, `ruff`, `mypy`, `zensical` (docs - deferred to Phase 6).

**Reference:** `/Users/mjsmith/dev-projects/ibx-uddi-sdk` has an analogous SDK. Read `src/ibx_uddi_sdk/_http.py`, `_resource.py`, `_exceptions.py`, `client.py` for pattern inspiration. **Do not copy verbatim** - the auth, `_ref`, pagination, and return-fields semantics differ.

**Spec:** `docs/superpowers/specs/2026-04-17-ibx-nios-sdk-design.md`

---

## File Structure (end state of this plan)

```
ibx-nios-sdk/
├── .github/workflows/ci.yml
├── .gitignore
├── CLAUDE.md
├── LICENSE                              # Apache-2.0
├── README.md
├── pyproject.toml
├── docs/superpowers/
│   ├── specs/2026-04-17-ibx-nios-sdk-design.md  (exists)
│   └── plans/2026-04-17-phase-0-1-foundation.md (this file)
├── schemas/v2.14/                       # swagger snapshots (stub for now)
│   └── README.md
├── src/ibx_nios_sdk/
│   ├── __init__.py                      # public exports
│   ├── py.typed                         # empty marker
│   ├── _version.py                      # __version__, default WAPI version
│   ├── _exceptions.py                   # NiosError hierarchy
│   ├── _http.py                         # HttpClient
│   ├── _query.py                        # WAPI query-param + filter-operator builder
│   ├── _paging.py                       # AsyncPageIterator
│   ├── _resource.py                     # WapiResource base
│   ├── client.py                        # NiosClient
│   └── _common/
│       ├── __init__.py
│       └── models.py                    # ExtAttr, ExtAttrValue shared models
└── tests/
    ├── __init__.py
    ├── conftest.py                      # make_http_client, mock handlers
    ├── test_imports.py                  # smoke test
    ├── test_exceptions.py
    ├── test_query.py
    ├── test_paging.py
    ├── test_resource.py
    ├── test_client.py
    └── _http/
        ├── __init__.py
        ├── test_session_auth.py
        ├── test_basic_auth.py
        ├── test_auth_retry.py
        ├── test_retry_backoff.py
        ├── test_tls.py
        └── test_return_fields.py
```

---

## Task 1: Initialize repository and scaffolding files

**Files:**
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `src/ibx_nios_sdk/__init__.py` (empty for now)
- Create: `src/ibx_nios_sdk/py.typed` (empty)
- Create: `src/ibx_nios_sdk/_version.py`
- Create: `tests/__init__.py` (empty)
- Create: `tests/conftest.py` (minimal, expanded later)
- Create: `schemas/v2.14/README.md`

- [ ] **Step 1.1: `git init` the repo**

Run:
```bash
cd /Users/mjsmith/dev-projects/ibx-nios-sdk
git init -b main
```

- [ ] **Step 1.2: Write `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
build/
dist/

# Virtualenv
.venv/
venv/

# IDE
.vscode/
.idea/

# Docs output
site/

# OS
.DS_Store
```

- [ ] **Step 1.3: Write `LICENSE` (Apache-2.0)**

Copy the full Apache-2.0 license text from https://www.apache.org/licenses/LICENSE-2.0.txt. Substitute "Infoblox" as the copyright holder and 2026 as the year in the appendix.

- [ ] **Step 1.4: Write `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=70.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ibx-nios-sdk"
version = "0.1.0"
description = "Python Client for Infoblox NIOS WAPI"
readme = "README.md"
license = "Apache-2.0"
requires-python = ">=3.11"
authors = [{ name = "Infoblox" }]
classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Operating System :: OS Independent",
    "Framework :: AsyncIO",
    "Typing :: Typed",
]
dependencies = [
    "httpx>=0.27",
    "pydantic>=2",
    "python-dateutil>=2.8.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5",
    "mypy>=1.10",
    "ruff>=0.5",
]

[project.urls]
Homepage = "https://github.com/Infoblox-PS/ibx-nios-sdk"
Repository = "https://github.com/Infoblox-PS/ibx-nios-sdk"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"*" = ["py.typed"]

[tool.ruff]
target-version = "py311"
line-length = 99

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM", "TCH"]
ignore = ["E501", "TC001", "TC002", "TC003", "SIM105"]

[tool.mypy]
python_version = "3.11"
strict = true
packages = ["ibx_nios_sdk"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
pythonpath = ["tests"]
```

- [ ] **Step 1.5: Write `README.md`**

````markdown
# ibx-nios-sdk

Async Python SDK for Infoblox NIOS WAPI v2.14.

> **Status:** 0.1.0 - foundation only. WAPI domain modules (DNS, DHCP, IPAM, Grid, ...) are being added in subsequent releases.

## Install

```bash
pip install ibx-nios-sdk
```

## Quickstart

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient(
        grid_url="https://grid.example.com",
        username="admin",
        password="infoblox",
    ) as client:
        print("connected to", client.grid_url)

asyncio.run(main())
```

See `docs/` for details.
````

- [ ] **Step 1.6: Write `src/ibx_nios_sdk/_version.py`**

```python
"""SDK version and WAPI version constants."""

from __future__ import annotations

__version__ = "0.1.0"
DEFAULT_WAPI_VERSION = "2.14"
```

- [ ] **Step 1.7: Write empty `src/ibx_nios_sdk/__init__.py`, `src/ibx_nios_sdk/py.typed`, `tests/__init__.py`, `tests/conftest.py`**

All four files are empty (zero-byte) for now. They will be populated in later tasks.

- [ ] **Step 1.8: Write `schemas/v2.14/README.md`**

```markdown
# NIOS WAPI v2.14 Swagger Snapshots

Swagger JSON snapshots sourced from:
https://infobloxopen.github.io/nios-swagger/swagger-ui/openspec/v2.14/

One file per domain: dns.json, dhcp.json, ipam.json, grid.json, rpz.json, dtc.json,
threatprotection.json, threatinsight.json, security.json, smartfolder.json, acl.json,
cloud.json, discovery.json, federatedrealms.json, microsoftserver.json, misc.json,
notification.json.

Populated in Phase 2 when we begin writing domain models. Kept for diff-checking
against future WAPI versions.
```

- [ ] **Step 1.9: Create virtualenv and install dev deps**

```bash
cd /Users/mjsmith/dev-projects/ibx-nios-sdk
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Expected: clean install, no errors.

- [ ] **Step 1.10: Run tooling - all must pass with zero findings**

```bash
source .venv/bin/activate
ruff check src/ tests/
ruff format --check src/ tests/
mypy
pytest
```

Expected:
- `ruff check`: "All checks passed!"
- `ruff format --check`: "N files already formatted"
- `mypy`: "Success: no issues found" (package has no .py files yet under `ibx_nios_sdk/` besides `_version.py`)
- `pytest`: "collected 0 items" exits 0

- [ ] **Step 1.11: Commit**

```bash
git add .
git commit -m "chore: initial project scaffolding"
```

---

## Task 2: Import smoke test

**Files:**
- Create: `tests/test_imports.py`

- [ ] **Step 2.1: Write failing test**

```python
# tests/test_imports.py
"""Smoke tests - verify the package is importable and exposes expected top-level names."""

from __future__ import annotations


def test_package_importable() -> None:
    import ibx_nios_sdk

    assert hasattr(ibx_nios_sdk, "__version__")
    assert ibx_nios_sdk.__version__ == "0.1.0"


def test_default_wapi_version() -> None:
    from ibx_nios_sdk._version import DEFAULT_WAPI_VERSION

    assert DEFAULT_WAPI_VERSION == "2.14"
```

- [ ] **Step 2.2: Run tests - first fails, second passes**

```bash
pytest tests/test_imports.py -v
```

Expected: `test_package_importable` FAILS (no `__version__` re-exported yet). `test_default_wapi_version` PASSES.

- [ ] **Step 2.3: Re-export `__version__` from package root**

Write `src/ibx_nios_sdk/__init__.py`:

```python
"""ibx-nios-sdk - async Python client for Infoblox NIOS WAPI."""

from __future__ import annotations

from ibx_nios_sdk._version import __version__

__all__ = ["__version__"]
```

- [ ] **Step 2.4: Run tests - both pass**

```bash
pytest tests/test_imports.py -v
```

Expected: 2 PASSED.

- [ ] **Step 2.5: Commit**

```bash
git add src/ibx_nios_sdk/__init__.py tests/test_imports.py
git commit -m "feat: package importable, re-export __version__"
```

---

## Task 3: Exception hierarchy

**Files:**
- Create: `src/ibx_nios_sdk/_exceptions.py`
- Create: `tests/test_exceptions.py`

- [ ] **Step 3.1: Write failing tests**

```python
# tests/test_exceptions.py
"""Tests for NiosError hierarchy and exception_for_status dispatcher."""

from __future__ import annotations

import pytest

from ibx_nios_sdk._exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NiosConnectionError,
    NiosError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    exception_for_status,
)


def test_base_carries_attrs() -> None:
    err = NiosError(status_code=500, message="boom", wapi_code="X", wapi_text="t")
    assert err.status_code == 500
    assert err.message == "boom"
    assert err.wapi_code == "X"
    assert err.wapi_text == "t"
    assert str(err) == "boom"


def test_hierarchy_subclasses_nios_error() -> None:
    for cls in (
        AuthenticationError,
        NotFoundError,
        BadRequestError,
        ConflictError,
        RateLimitError,
        ServerError,
        ValidationError,
        NiosConnectionError,
    ):
        assert issubclass(cls, NiosError)


@pytest.mark.parametrize(
    ("status", "expected_cls"),
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (404, NotFoundError),
        (409, ConflictError),
        (429, RateLimitError),
        (500, ServerError),
        (502, ServerError),
        (503, ServerError),
        (599, ServerError),
    ],
)
def test_exception_for_status_dispatch(status: int, expected_cls: type) -> None:
    err = exception_for_status(status, "msg", {"Error": "details", "code": "C", "text": "T"})
    assert isinstance(err, expected_cls)
    assert err.status_code == status


def test_exception_for_status_extracts_wapi_fields() -> None:
    err = exception_for_status(400, "msg", {"Error": "bad", "code": "Client.Ibap.Data", "text": "field x"})
    assert err.wapi_code == "Client.Ibap.Data"
    assert err.wapi_text == "field x"


def test_exception_for_status_unknown_returns_base() -> None:
    err = exception_for_status(418, "teapot", None)
    assert type(err) is NiosError
    assert err.status_code == 418


def test_rate_limit_retry_after() -> None:
    err = exception_for_status(429, "rate", None, retry_after=5.0)
    assert isinstance(err, RateLimitError)
    assert err.retry_after == 5.0
```

- [ ] **Step 3.2: Run tests - verify they fail**

```bash
pytest tests/test_exceptions.py -v
```

Expected: all FAIL with `ModuleNotFoundError` on `ibx_nios_sdk._exceptions`.

- [ ] **Step 3.3: Implement `_exceptions.py`**

```python
# src/ibx_nios_sdk/_exceptions.py
"""Domain-aware exception hierarchy for the NIOS SDK."""

from __future__ import annotations

from typing import Any


class NiosError(Exception):
    """Base exception for all NIOS SDK errors."""

    def __init__(
        self,
        *,
        status_code: int | None = None,
        message: str,
        response_body: dict[str, Any] | None = None,
        wapi_code: str | None = None,
        wapi_text: str | None = None,
        request_url: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        self.wapi_code = wapi_code
        self.wapi_text = wapi_text
        self.request_url = request_url
        super().__init__(message)


class NiosConnectionError(NiosError):
    """TLS failure, DNS failure, connect timeout - pre-HTTP-response errors."""


class AuthenticationError(NiosError):
    """401 - credentials rejected or session expired."""


class NotFoundError(NiosError):
    """404 - object does not exist."""


class BadRequestError(NiosError):
    """400 - malformed request or invalid field values."""


class ConflictError(NiosError):
    """409 - object already exists or state conflict."""


class RateLimitError(NiosError):
    """429 - too many requests."""

    def __init__(
        self,
        *,
        status_code: int | None = None,
        message: str,
        response_body: dict[str, Any] | None = None,
        wapi_code: str | None = None,
        wapi_text: str | None = None,
        request_url: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            message=message,
            response_body=response_body,
            wapi_code=wapi_code,
            wapi_text=wapi_text,
            request_url=request_url,
        )
        self.retry_after = retry_after


class ServerError(NiosError):
    """5xx - server-side failure."""


class ValidationError(NiosError):
    """Pydantic parse failure - response did not match the expected model."""


_STATUS_MAP: dict[int, type[NiosError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    404: NotFoundError,
    409: ConflictError,
    429: RateLimitError,
}


def _extract_wapi_fields(body: dict[str, Any] | None) -> tuple[str | None, str | None]:
    if not isinstance(body, dict):
        return None, None
    return body.get("code"), body.get("text")


def exception_for_status(
    status_code: int,
    message: str,
    response_body: dict[str, Any] | None,
    *,
    retry_after: float | None = None,
    request_url: str | None = None,
) -> NiosError:
    """Dispatch a status code to the right NiosError subclass."""
    wapi_code, wapi_text = _extract_wapi_fields(response_body)

    exc_class = _STATUS_MAP.get(status_code)
    if exc_class is None:
        if 500 <= status_code < 600:
            exc_class = ServerError
        else:
            return NiosError(
                status_code=status_code,
                message=message,
                response_body=response_body,
                wapi_code=wapi_code,
                wapi_text=wapi_text,
                request_url=request_url,
            )

    if exc_class is RateLimitError:
        return RateLimitError(
            status_code=status_code,
            message=message,
            response_body=response_body,
            wapi_code=wapi_code,
            wapi_text=wapi_text,
            request_url=request_url,
            retry_after=retry_after,
        )

    return exc_class(
        status_code=status_code,
        message=message,
        response_body=response_body,
        wapi_code=wapi_code,
        wapi_text=wapi_text,
        request_url=request_url,
    )
```

- [ ] **Step 3.4: Run tests - all pass**

```bash
pytest tests/test_exceptions.py -v
```

Expected: all PASSED.

- [ ] **Step 3.5: Run mypy + ruff**

```bash
mypy
ruff check src/ tests/
```

Expected: zero findings.

- [ ] **Step 3.6: Commit**

```bash
git add src/ibx_nios_sdk/_exceptions.py tests/test_exceptions.py
git commit -m "feat: add NiosError hierarchy with status-code dispatcher"
```

---

## Task 4: Common shared models (`ExtAttrValue`, `ExtAttr`)

**Files:**
- Create: `src/ibx_nios_sdk/_common/__init__.py`
- Create: `src/ibx_nios_sdk/_common/models.py`
- Create: `tests/test_common_models.py`

- [ ] **Step 4.1: Write failing tests**

```python
# tests/test_common_models.py
"""Tests for shared cross-domain models."""

from __future__ import annotations

from ibx_nios_sdk._common.models import ExtAttrValue


def test_extattr_value_value_only() -> None:
    ea = ExtAttrValue.model_validate({"value": "NYC"})
    assert ea.value == "NYC"
    assert ea.inheritance_source is None


def test_extattr_value_with_inheritance() -> None:
    payload = {
        "value": "NYC",
        "inheritance_source": {"_ref": "network/abc:10.0.0.0/8/default"},
    }
    ea = ExtAttrValue.model_validate(payload)
    assert ea.value == "NYC"
    assert ea.inheritance_source == {"_ref": "network/abc:10.0.0.0/8/default"}


def test_extattr_value_serialize_excludes_none() -> None:
    ea = ExtAttrValue(value="NYC")
    dumped = ea.model_dump(exclude_none=True)
    assert dumped == {"value": "NYC"}


def test_extattr_value_extra_fields_allowed() -> None:
    ea = ExtAttrValue.model_validate({"value": "NYC", "descendants_action": {"option_with_ea": "INHERIT"}})
    assert ea.value == "NYC"
```

- [ ] **Step 4.2: Run tests - verify they fail**

```bash
pytest tests/test_common_models.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 4.3: Implement `_common/__init__.py`**

```python
# src/ibx_nios_sdk/_common/__init__.py
"""Cross-domain shared types for the NIOS SDK."""

from __future__ import annotations

from ibx_nios_sdk._common.models import ExtAttrValue

__all__ = ["ExtAttrValue"]
```

- [ ] **Step 4.4: Implement `_common/models.py`**

```python
# src/ibx_nios_sdk/_common/models.py
"""Cross-domain pydantic models shared across all WAPI domains."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ExtAttrValue(BaseModel):
    """Extensible-attribute value with optional inheritance metadata.

    WAPI shape:
        {"value": "NYC", "inheritance_source": {"_ref": "..."}}

    ``inheritance_source`` is only populated when the caller requested it
    via ``return_fields_plus=[..., "extattrs.<name>.inheritance_source"]``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    value: str | int | bool | float
    inheritance_source: dict[str, Any] | None = None
```

- [ ] **Step 4.5: Run tests - all pass**

```bash
pytest tests/test_common_models.py -v
mypy
ruff check src/ tests/
```

Expected: 4 PASSED, mypy/ruff clean.

- [ ] **Step 4.6: Commit**

```bash
git add src/ibx_nios_sdk/_common/ tests/test_common_models.py
git commit -m "feat: add ExtAttrValue shared model"
```

---

## Task 5: WAPI query-param builder (`_query.py`)

**Purpose:** Translate Python kwargs into WAPI query params, including filter operators (`name__like=` → `name~=`) and return-field handling.

**Files:**
- Create: `src/ibx_nios_sdk/_query.py`
- Create: `tests/test_query.py`

- [ ] **Step 5.1: Write failing tests**

```python
# tests/test_query.py
"""Tests for the WAPI query-param builder."""

from __future__ import annotations

import pytest

from ibx_nios_sdk._query import build_filter_params, build_return_fields_params


def test_exact_filter() -> None:
    assert build_filter_params({"name": "host.example.com"}) == {"name": "host.example.com"}


def test_like_operator() -> None:
    assert build_filter_params({"name__like": "host"}) == {"name~": "host"}


def test_comparison_operators() -> None:
    assert build_filter_params({"count__gte": 5}) == {"count>": "5"}
    assert build_filter_params({"count__lte": 5}) == {"count<": "5"}
    assert build_filter_params({"name__not": "x"}) == {"name!": "x"}


def test_extattr_filter() -> None:
    assert build_filter_params({"extattr_Site": "NYC"}) == {"*Site": "NYC"}


def test_none_values_dropped() -> None:
    assert build_filter_params({"name": None, "view": "default"}) == {"view": "default"}


def test_unknown_operator_raises() -> None:
    with pytest.raises(ValueError, match="unknown filter operator"):
        build_filter_params({"name__weird": "x"})


def test_bool_values_lowercased() -> None:
    assert build_filter_params({"disable": True, "locked": False}) == {
        "disable": "true",
        "locked": "false",
    }


def test_return_fields_default_model_fields() -> None:
    params = build_return_fields_params(
        model_fields=["name", "view"], return_fields=None, return_fields_plus=None
    )
    assert params == {"_return_fields+": "name,view"}


def test_return_fields_exact() -> None:
    params = build_return_fields_params(
        model_fields=["name", "view"], return_fields=["name"], return_fields_plus=None
    )
    assert params == {"_return_fields": "name"}


def test_return_fields_plus() -> None:
    params = build_return_fields_params(
        model_fields=["name"], return_fields=None, return_fields_plus=["extattrs"]
    )
    assert params == {"_return_fields+": "name,extattrs"}


def test_return_fields_both_raises() -> None:
    with pytest.raises(ValueError, match="cannot pass both"):
        build_return_fields_params(
            model_fields=["name"], return_fields=["name"], return_fields_plus=["x"]
        )


def test_return_fields_empty_model_fields_plus_only() -> None:
    params = build_return_fields_params(
        model_fields=[], return_fields=None, return_fields_plus=["extattrs"]
    )
    assert params == {"_return_fields+": "extattrs"}
```

- [ ] **Step 5.2: Run tests - verify they fail**

```bash
pytest tests/test_query.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 5.3: Implement `_query.py`**

```python
# src/ibx_nios_sdk/_query.py
"""Translate Python kwargs into WAPI query parameters.

WAPI operator conventions:
  field=value       -> exact match
  field~=value      -> regex/substring match   (kwarg: field__like)
  field<=value      -> less than or equal       (kwarg: field__lte)
  field>=value      -> greater than or equal    (kwarg: field__gte)
  field!=value      -> not equal                (kwarg: field__not)
  *EA_name=value    -> extensible-attr filter   (kwarg: extattr_EA_name)
"""

from __future__ import annotations

from typing import Any

_OPERATOR_SUFFIX_MAP: dict[str, str] = {
    "like": "~",
    "gte": ">",
    "lte": "<",
    "not": "!",
}


def _stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_filter_params(filters: dict[str, Any]) -> dict[str, str]:
    """Translate kwarg-style filters into WAPI query-param key/value pairs.

    Keys with a ``__<op>`` suffix map to the corresponding WAPI operator.
    Keys prefixed ``extattr_`` map to ``*<EA_name>``.
    ``None`` values are dropped.

    Raises:
        ValueError: if an unknown ``__<op>`` suffix is used.
    """
    out: dict[str, str] = {}
    for key, value in filters.items():
        if value is None:
            continue

        if key.startswith("extattr_"):
            ea_name = key[len("extattr_"):]
            out[f"*{ea_name}"] = _stringify(value)
            continue

        if "__" in key:
            field, _, suffix = key.rpartition("__")
            op = _OPERATOR_SUFFIX_MAP.get(suffix)
            if op is None:
                raise ValueError(f"unknown filter operator: {suffix!r} in kwarg {key!r}")
            out[f"{field}{op}"] = _stringify(value)
            continue

        out[key] = _stringify(value)

    return out


def build_return_fields_params(
    *,
    model_fields: list[str],
    return_fields: list[str] | None,
    return_fields_plus: list[str] | None,
) -> dict[str, str]:
    """Build the ``_return_fields`` / ``_return_fields+`` query params.

    - Both None   -> send ``_return_fields+=<model_fields>`` so the full model populates.
    - ``return_fields=[..]`` -> send ``_return_fields=<exact list>``.
    - ``return_fields_plus=[..]`` -> send ``_return_fields+=<model_fields + extras>``.
    - Passing both -> ``ValueError``.
    """
    if return_fields is not None and return_fields_plus is not None:
        raise ValueError("cannot pass both return_fields and return_fields_plus")

    if return_fields is not None:
        return {"_return_fields": ",".join(return_fields)}

    combined = list(model_fields)
    if return_fields_plus:
        combined.extend(return_fields_plus)
    if not combined:
        return {}
    return {"_return_fields+": ",".join(combined)}
```

- [ ] **Step 5.4: Run tests - all pass**

```bash
pytest tests/test_query.py -v
mypy
ruff check src/ tests/
```

Expected: all PASSED, mypy/ruff clean.

- [ ] **Step 5.5: Commit**

```bash
git add src/ibx_nios_sdk/_query.py tests/test_query.py
git commit -m "feat: add WAPI query-param builder with filter operators"
```

---

## Task 6: `HttpClient` core - init, TLS, basic request/response plumbing

**Purpose:** Build the skeleton that handles `base_url`, TLS config, request dispatch, response parsing, and error wrapping. Auth comes in Task 7.

**Files:**
- Create: `src/ibx_nios_sdk/_http.py`
- Modify: `tests/conftest.py`
- Create: `tests/_http/__init__.py`
- Create: `tests/_http/test_tls.py` (just the non-auth parts of TLS behavior for now)

- [ ] **Step 6.1: Expand `tests/conftest.py` with reusable helpers**

```python
# tests/conftest.py
"""Shared test fixtures and helpers for ibx-nios-sdk tests."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import httpx

from ibx_nios_sdk._http import HttpClient


def json_response(payload: Any, status_code: int = 200, headers: dict[str, str] | None = None) -> httpx.Response:
    """Build an httpx.Response with a JSON body - used in MockTransport handlers."""
    return httpx.Response(
        status_code=status_code,
        content=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **(headers or {})},
    )


Handler = Callable[[httpx.Request], httpx.Response]


def make_http_client(
    handler: Handler,
    *,
    grid_url: str = "https://grid.example.com",
    username: str = "admin",
    password: str = "infoblox",
    wapi_version: str = "2.14",
    use_session: bool = True,
    verify: bool | str = True,
    max_retries: int = 3,
) -> HttpClient:
    """Build an HttpClient backed by an httpx.MockTransport handler."""
    return HttpClient(
        grid_url=grid_url,
        username=username,
        password=password,
        wapi_version=wapi_version,
        use_session=use_session,
        verify=verify,
        max_retries=max_retries,
        transport=httpx.MockTransport(handler),
    )
```

- [ ] **Step 6.2: Write failing TLS-error-wrapping test**

```python
# tests/_http/__init__.py
# (empty)
```

```python
# tests/_http/test_tls.py
"""TLS/connect-error wrapping behavior for HttpClient."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import NiosConnectionError
from tests.conftest import make_http_client


async def test_tls_error_wrapped_with_helpful_message() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED] self signed certificate")

    client = make_http_client(handler)
    try:
        with pytest.raises(NiosConnectionError) as exc_info:
            await client.request("GET", "/grid")
        msg = exc_info.value.message
        assert "TLS verification failed" in msg
        assert "verify=False" in msg
        assert "ca_bundle" in msg
    finally:
        await client.aclose()


async def test_non_tls_connect_error_also_wrapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Name or service not known")

    client = make_http_client(handler)
    try:
        with pytest.raises(NiosConnectionError):
            await client.request("GET", "/grid")
    finally:
        await client.aclose()
```

- [ ] **Step 6.3: Run tests - verify they fail**

```bash
pytest tests/_http/test_tls.py -v
```

Expected: FAIL with `ModuleNotFoundError` on `ibx_nios_sdk._http`.

- [ ] **Step 6.4: Implement `_http.py` skeleton**

```python
# src/ibx_nios_sdk/_http.py
"""HTTP client for Infoblox NIOS WAPI, built on httpx.AsyncClient."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import httpx

from ibx_nios_sdk._exceptions import NiosConnectionError, exception_for_status
from ibx_nios_sdk._version import DEFAULT_WAPI_VERSION, __version__

logger = logging.getLogger("ibx_nios_sdk")

_log_level = os.environ.get("IB_LOG_LEVEL", "").upper()
if _log_level == "DEBUG":  # pragma: no cover
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)


def _is_tls_error(exc: httpx.ConnectError) -> bool:
    msg = str(exc).lower()
    return "ssl" in msg or "certificate" in msg or "tls" in msg


class HttpClient:
    """Async HTTP client for Infoblox NIOS WAPI."""

    def __init__(
        self,
        *,
        grid_url: str,
        username: str,
        password: str,
        wapi_version: str = DEFAULT_WAPI_VERSION,
        use_session: bool = True,
        verify: bool | str | Path = True,
        timeout: float = 30.0,
        max_retries: int = 3,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._grid_url = grid_url.rstrip("/")
        self._username = username
        self._password = password
        self._wapi_version = wapi_version
        self._use_session = use_session
        self._max_retries = max_retries
        self._logged_in = False

        client_kwargs: dict[str, Any] = {
            "base_url": f"{self._grid_url}/wapi/v{wapi_version}",
            "timeout": timeout,
            "verify": verify,
            "headers": {
                "Content-Type": "application/json",
                "x-infoblox-client": "ibx-nios-sdk",
                "x-infoblox-sdk": f"python/{__version__}",
            },
        }
        if transport is not None:
            client_kwargs["transport"] = transport

        self._client = httpx.AsyncClient(**client_kwargs)

    @property
    def grid_url(self) -> str:
        return self._grid_url

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Send a request, handle response, raise on error. No auth/retry yet."""
        url = path if path.startswith("/") else f"/{path}"
        logger.debug("%s %s%s params=%s", method, self._client.base_url, url, params)
        try:
            response = await self._client.request(method, url, params=params, json=json)
        except httpx.ConnectError as exc:
            if _is_tls_error(exc):
                raise NiosConnectionError(
                    message=(
                        f"TLS verification failed against {self._grid_url}. "
                        "For self-signed certs, pass verify=False or "
                        "ca_bundle=/path/to/ca.pem. "
                        f"Underlying error: {exc}"
                    ),
                ) from exc
            raise NiosConnectionError(
                message=f"Connection failed to {self._grid_url}: {exc}",
            ) from exc

        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict[str, Any] | None:
        if response.status_code == 204:
            return None

        body: dict[str, Any] | None = None
        try:
            parsed = response.json()
            if isinstance(parsed, dict):
                body = parsed
            else:
                # WAPI sometimes returns a bare string (e.g., delete returns the _ref)
                body = {"_value": parsed}
        except Exception:
            body = None

        if response.is_success:
            return body

        message = _extract_error_message(body) or response.reason_phrase or f"HTTP {response.status_code}"
        raise exception_for_status(
            response.status_code,
            message,
            body,
            request_url=str(response.request.url),
        )

    async def aclose(self) -> None:
        await self._client.aclose()


def _extract_error_message(body: dict[str, Any] | None) -> str | None:
    if not isinstance(body, dict):
        return None
    # WAPI standard error shape: {"Error": "...", "code": "...", "text": "..."}
    err = body.get("Error") or body.get("text")
    if isinstance(err, str):
        return err
    return None
```

- [ ] **Step 6.5: Run TLS tests - pass**

```bash
pytest tests/_http/test_tls.py -v
mypy
ruff check src/ tests/
```

Expected: 2 PASSED, mypy/ruff clean.

- [ ] **Step 6.6: Commit**

```bash
git add src/ibx_nios_sdk/_http.py tests/conftest.py tests/_http/
git commit -m "feat: add HttpClient skeleton with TLS error wrapping"
```

---

## Task 7: Session-cookie auth (login, logout, 401 auto-retry)

**Files:**
- Modify: `src/ibx_nios_sdk/_http.py`
- Create: `tests/_http/test_session_auth.py`
- Create: `tests/_http/test_auth_retry.py`

- [ ] **Step 7.1: Write failing session-auth tests**

```python
# tests/_http/test_session_auth.py
"""Session-cookie authentication: lazy login, cookie reuse, logout on close."""

from __future__ import annotations

import base64

import httpx

from tests.conftest import json_response, make_http_client


async def test_lazy_login_on_first_request() -> None:
    calls: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append((request.method, request.url.path))
        if request.url.path.endswith("/grid/session"):
            auth = request.headers.get("Authorization", "")
            assert auth.startswith("Basic "), "login should send HTTP Basic credentials"
            decoded = base64.b64decode(auth.removeprefix("Basic ")).decode()
            assert decoded == "admin:infoblox"
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=session-token-123; Path=/"},
            )
        # Subsequent calls must carry the cookie, not basic auth.
        assert "Authorization" not in request.headers or not request.headers["Authorization"].startswith("Basic ")
        assert "ibapauth=session-token-123" in request.headers.get("Cookie", "")
        return json_response({"_ref": "grid/b25lLmNsdXN0ZXIkMA:Infoblox"})

    client = make_http_client(handler)
    try:
        await client.request("GET", "/grid")
        # Login call was made exactly once + the actual /grid call = 2 total.
        assert len(calls) == 2
        assert calls[0][1].endswith("/grid/session")

        # Second request should reuse the cookie, not re-login.
        await client.request("GET", "/grid")
        assert len(calls) == 3
        assert calls[2][1].endswith("/grid")
    finally:
        await client.aclose()


async def test_logout_on_close() -> None:
    logout_called = False

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal logout_called
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        if request.url.path.endswith("/logout"):
            logout_called = True
            return httpx.Response(200, json={})
        return json_response({})

    client = make_http_client(handler)
    await client.request("GET", "/grid")
    await client.aclose()
    assert logout_called
```

```python
# tests/_http/test_auth_retry.py
"""401 auto-retry: one transparent re-login after 401, then propagate."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import AuthenticationError
from tests.conftest import json_response, make_http_client


async def test_401_triggers_single_relogin() -> None:
    login_count = 0
    grid_401_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal login_count, grid_401_count
        if request.url.path.endswith("/grid/session"):
            login_count += 1
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": f"ibapauth=token-{login_count}; Path=/"},
            )
        if request.url.path.endswith("/grid"):
            if grid_401_count == 0:
                grid_401_count += 1
                return json_response({"Error": "Session expired"}, status_code=401)
            return json_response({"_ref": "grid/b25l:Infoblox"})
        return json_response({})

    client = make_http_client(handler)
    try:
        data = await client.request("GET", "/grid")
        assert data == {"_ref": "grid/b25l:Infoblox"}
        assert login_count == 2, "initial login + one re-login"
        assert grid_401_count == 1
    finally:
        await client.aclose()


async def test_second_401_raises_authentication_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        return json_response({"Error": "bad creds"}, status_code=401)

    client = make_http_client(handler)
    try:
        with pytest.raises(AuthenticationError):
            await client.request("GET", "/grid")
    finally:
        await client.aclose()
```

- [ ] **Step 7.2: Run tests - verify they fail**

```bash
pytest tests/_http/test_session_auth.py tests/_http/test_auth_retry.py -v
```

Expected: all FAIL (login not wired in, 401 not retried).

- [ ] **Step 7.3: Add session login/logout/auth-retry to `_http.py`**

Modify `src/ibx_nios_sdk/_http.py`. Replace the existing `HttpClient` class with:

```python
class HttpClient:
    """Async HTTP client for Infoblox NIOS WAPI."""

    def __init__(
        self,
        *,
        grid_url: str,
        username: str,
        password: str,
        wapi_version: str = DEFAULT_WAPI_VERSION,
        use_session: bool = True,
        verify: bool | str | Path = True,
        timeout: float = 30.0,
        max_retries: int = 3,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._grid_url = grid_url.rstrip("/")
        self._username = username
        self._password = password
        self._wapi_version = wapi_version
        self._use_session = use_session
        self._max_retries = max_retries
        self._logged_in = False

        client_kwargs: dict[str, Any] = {
            "base_url": f"{self._grid_url}/wapi/v{wapi_version}",
            "timeout": timeout,
            "verify": verify,
            "headers": {
                "Content-Type": "application/json",
                "x-infoblox-client": "ibx-nios-sdk",
                "x-infoblox-sdk": f"python/{__version__}",
            },
        }
        if not use_session:
            client_kwargs["auth"] = httpx.BasicAuth(username, password)
        if transport is not None:
            client_kwargs["transport"] = transport

        self._client = httpx.AsyncClient(**client_kwargs)

    @property
    def grid_url(self) -> str:
        return self._grid_url

    async def _login(self) -> None:
        """Open a WAPI session. Sets the ibapauth cookie in the cookie jar."""
        response = await self._client.get(
            "/grid/session",
            auth=httpx.BasicAuth(self._username, self._password),
        )
        if response.status_code == 401:
            raise exception_for_status(
                401,
                "NIOS login failed: bad credentials",
                _safe_json(response),
                request_url=str(response.request.url),
            )
        response.raise_for_status()
        self._logged_in = True

    async def _logout(self) -> None:
        """Invalidate the WAPI session server-side. Best-effort; swallow errors."""
        try:
            await self._client.post("/logout")
        except Exception:
            pass
        self._logged_in = False

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Send a request with lazy-login + one-shot 401 re-login."""
        if self._use_session and not self._logged_in:
            await self._login()

        url = path if path.startswith("/") else f"/{path}"
        response = await self._send(method, url, params=params, json=json)

        # One-shot 401 re-login (session mode only).
        if (
            self._use_session
            and response.status_code == 401
            and self._logged_in
            and not url.endswith("/grid/session")
        ):
            logger.debug("401 on %s - re-logging in", url)
            self._logged_in = False
            await self._login()
            response = await self._send(method, url, params=params, json=json)

        return self._handle_response(response)

    async def _send(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        logger.debug("%s %s%s params=%s", method, self._client.base_url, url, params)
        try:
            return await self._client.request(method, url, params=params, json=json)
        except httpx.ConnectError as exc:
            if _is_tls_error(exc):
                raise NiosConnectionError(
                    message=(
                        f"TLS verification failed against {self._grid_url}. "
                        "For self-signed certs, pass verify=False or "
                        "ca_bundle=/path/to/ca.pem. "
                        f"Underlying error: {exc}"
                    ),
                ) from exc
            raise NiosConnectionError(
                message=f"Connection failed to {self._grid_url}: {exc}",
            ) from exc

    def _handle_response(self, response: httpx.Response) -> dict[str, Any] | None:
        if response.status_code == 204:
            return None

        body = _safe_json(response)

        if response.is_success:
            return body

        message = (
            _extract_error_message(body)
            or response.reason_phrase
            or f"HTTP {response.status_code}"
        )
        raise exception_for_status(
            response.status_code,
            message,
            body,
            request_url=str(response.request.url),
        )

    async def aclose(self) -> None:
        if self._use_session and self._logged_in:
            await self._logout()
        await self._client.aclose()


def _safe_json(response: httpx.Response) -> dict[str, Any] | None:
    try:
        parsed = response.json()
    except Exception:
        return None
    if isinstance(parsed, dict):
        return parsed
    return {"_value": parsed}
```

- [ ] **Step 7.4: Run all HTTP tests - pass**

```bash
pytest tests/_http/ -v
mypy
ruff check src/ tests/
```

Expected: all PASSED.

- [ ] **Step 7.5: Commit**

```bash
git add src/ibx_nios_sdk/_http.py tests/_http/
git commit -m "feat: session-cookie auth, lazy login, 401 auto-retry, logout on close"
```

---

## Task 8: Basic-auth mode + retry backoff on 429/502/503/504

**Files:**
- Modify: `src/ibx_nios_sdk/_http.py`
- Create: `tests/_http/test_basic_auth.py`
- Create: `tests/_http/test_retry_backoff.py`

- [ ] **Step 8.1: Write failing tests**

```python
# tests/_http/test_basic_auth.py
"""Basic-auth mode: no login call, credentials sent per request via httpx BasicAuth."""

from __future__ import annotations

import base64

import httpx

from tests.conftest import json_response, make_http_client


async def test_basic_auth_mode_skips_login() -> None:
    paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        auth = request.headers.get("Authorization", "")
        assert auth.startswith("Basic ")
        decoded = base64.b64decode(auth.removeprefix("Basic ")).decode()
        assert decoded == "admin:infoblox"
        return json_response({"_ref": "grid/x:g"})

    client = make_http_client(handler, use_session=False)
    try:
        await client.request("GET", "/grid")
        assert not any(p.endswith("/grid/session") for p in paths)
    finally:
        await client.aclose()
```

```python
# tests/_http/test_retry_backoff.py
"""Exponential backoff + Retry-After on 429, 502, 503, 504. No retry on 500."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk._exceptions import RateLimitError, ServerError
from tests.conftest import json_response, make_http_client


async def test_retry_on_503_then_success(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", fake_sleep)

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        if calls < 3:
            return json_response({"Error": "busy"}, status_code=503)
        return json_response({"_ref": "grid/x:g"})

    client = make_http_client(handler)
    try:
        data = await client.request("GET", "/grid")
        assert data == {"_ref": "grid/x:g"}
        assert calls == 3
        assert len(sleeps) == 2
    finally:
        await client.aclose()


async def test_retry_after_header_respected(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", fake_sleep)

    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        if calls == 1:
            return httpx.Response(
                429,
                json={"Error": "rate"},
                headers={"Retry-After": "2", "Content-Type": "application/json"},
            )
        return json_response({"_ref": "grid/x:g"})

    client = make_http_client(handler)
    try:
        await client.request("GET", "/grid")
        assert sleeps == [2.0]
    finally:
        await client.aclose()


async def test_500_not_retried() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls += 1
        return json_response({"Error": "nope"}, status_code=500)

    client = make_http_client(handler, max_retries=3)
    try:
        with pytest.raises(ServerError):
            await client.request("GET", "/grid")
        assert calls == 1
    finally:
        await client.aclose()


async def test_retries_exhausted_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_sleep(delay: float) -> None:
        return None

    monkeypatch.setattr("ibx_nios_sdk._http.asyncio.sleep", fake_sleep)

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        return httpx.Response(429, json={"Error": "rate"}, headers={"Retry-After": "0"})

    client = make_http_client(handler, max_retries=2)
    try:
        with pytest.raises(RateLimitError):
            await client.request("GET", "/grid")
    finally:
        await client.aclose()
```

- [ ] **Step 8.2: Run tests - verify they fail**

```bash
pytest tests/_http/test_basic_auth.py tests/_http/test_retry_backoff.py -v
```

Expected: basic-auth test may pass (httpx `auth=` already wired); retry tests FAIL.

- [ ] **Step 8.3: Add retry logic to `_http.py`**

Add this import at the top of `_http.py`:

```python
import asyncio
```

Add the retry helpers after `_is_tls_error`:

```python
_RETRYABLE_STATUSES: frozenset[int] = frozenset({429, 502, 503, 504})


def _parse_retry_after(response: httpx.Response) -> float | None:
    ra = response.headers.get("Retry-After")
    if not ra:
        return None
    try:
        return float(ra)
    except ValueError:
        return None
```

Replace the existing `request()` method with:

```python
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Send a request with lazy-login, retry on 429/5xx, one-shot 401 re-login."""
        if self._use_session and not self._logged_in:
            await self._login()

        url = path if path.startswith("/") else f"/{path}"
        response = await self._request_with_retry(method, url, params=params, json=json)

        if (
            self._use_session
            and response.status_code == 401
            and self._logged_in
            and not url.endswith("/grid/session")
        ):
            logger.debug("401 on %s - re-logging in", url)
            self._logged_in = False
            await self._login()
            response = await self._request_with_retry(method, url, params=params, json=json)

        return self._handle_response(response)

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        for attempt in range(1 + self._max_retries):
            response = await self._send(method, url, params=params, json=json)
            if response.status_code not in _RETRYABLE_STATUSES or attempt >= self._max_retries:
                return response

            delay = _parse_retry_after(response)
            if delay is None or delay <= 0:
                delay = min(2**attempt * 0.5, 30.0)

            logger.debug(
                "Retrying %s %s (attempt %d/%d, status %d, delay %.1fs)",
                method, url, attempt + 1, self._max_retries, response.status_code, delay,
            )
            await asyncio.sleep(delay)

        raise AssertionError("unreachable")  # pragma: no cover
```

- [ ] **Step 8.4: Run all HTTP tests - pass**

```bash
pytest tests/_http/ -v
mypy
ruff check src/ tests/
```

Expected: all PASSED (basic-auth, session-auth, auth-retry, retry-backoff, tls).

- [ ] **Step 8.5: Commit**

```bash
git add src/ibx_nios_sdk/_http.py tests/_http/
git commit -m "feat: retry backoff on 429/502/503/504 with Retry-After support"
```

---

## Task 9: `_return_fields` injection at HttpClient level

**Purpose:** Give `HttpClient.get()` a dedicated path that merges model-default return fields into query params using `_query.build_return_fields_params`. Used by every resource.

**Files:**
- Modify: `src/ibx_nios_sdk/_http.py`
- Create: `tests/_http/test_return_fields.py`

- [ ] **Step 9.1: Write failing tests**

```python
# tests/_http/test_return_fields.py
"""HttpClient integrates _return_fields via build_return_fields_params."""

from __future__ import annotations

import httpx

from tests.conftest import json_response, make_http_client


async def _session_handler(store: dict[str, httpx.Request]) -> None:
    """Helper: no-op - see individual tests."""


async def test_get_auto_adds_return_fields_plus() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name", "ipv4addr", "view"],
        )
        req = captured[0]
        assert req.url.params["_return_fields+"] == "name,ipv4addr,view"
    finally:
        await client.aclose()


async def test_get_with_explicit_return_fields() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name", "ipv4addr"],
            return_fields=["name"],
        )
        req = captured[0]
        assert req.url.params["_return_fields"] == "name"
        assert "_return_fields+" not in req.url.params
    finally:
        await client.aclose()


async def test_get_with_return_fields_plus_extends() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response([])

    client = make_http_client(handler)
    try:
        await client.get_with_return_fields(
            "/record:a",
            model_fields=["name", "ipv4addr"],
            return_fields_plus=["extattrs"],
        )
        req = captured[0]
        assert req.url.params["_return_fields+"] == "name,ipv4addr,extattrs"
    finally:
        await client.aclose()
```

- [ ] **Step 9.2: Run tests - verify they fail**

```bash
pytest tests/_http/test_return_fields.py -v
```

Expected: FAIL - `HttpClient.get_with_return_fields` does not exist.

- [ ] **Step 9.3: Add `get_with_return_fields` and plain HTTP verbs to `HttpClient`**

Add these methods to `HttpClient` (after `request()`):

```python
    async def get(
        self, path: str, *, params: dict[str, str] | None = None
    ) -> dict[str, Any] | None:
        return await self.request("GET", path, params=params)

    async def post(
        self, path: str, *, params: dict[str, str] | None = None, json: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        return await self.request("POST", path, params=params, json=json)

    async def put(
        self, path: str, *, params: dict[str, str] | None = None, json: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        return await self.request("PUT", path, params=params, json=json)

    async def delete(
        self, path: str, *, params: dict[str, str] | None = None
    ) -> dict[str, Any] | None:
        return await self.request("DELETE", path, params=params)

    async def get_with_return_fields(
        self,
        path: str,
        *,
        model_fields: list[str],
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        extra_params: dict[str, str] | None = None,
    ) -> dict[str, Any] | None:
        """GET with `_return_fields` / `_return_fields+` merged in."""
        from ibx_nios_sdk._query import build_return_fields_params

        params = build_return_fields_params(
            model_fields=model_fields,
            return_fields=return_fields,
            return_fields_plus=return_fields_plus,
        )
        if extra_params:
            params.update(extra_params)
        return await self.request("GET", path, params=params or None)
```

- [ ] **Step 9.4: Run tests - pass**

```bash
pytest tests/_http/ -v
mypy
ruff check src/ tests/
```

Expected: all PASSED.

- [ ] **Step 9.5: Commit**

```bash
git add src/ibx_nios_sdk/_http.py tests/_http/test_return_fields.py
git commit -m "feat: HttpClient.get_with_return_fields injects _return_fields params"
```

---

## Task 10: `AsyncPageIterator`

**Files:**
- Create: `src/ibx_nios_sdk/_paging.py`
- Create: `tests/test_paging.py`

- [ ] **Step 10.1: Write failing tests**

```python
# tests/test_paging.py
"""AsyncPageIterator: transparent multi-page iteration across WAPI _paging responses."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

import pytest
from pydantic import BaseModel

from ibx_nios_sdk._paging import AsyncPageIterator


class Item(BaseModel):
    _ref: str = ""
    name: str


def make_fetcher(pages: list[tuple[list[dict[str, Any]], str | None]]) -> tuple[
    Callable[[str | None], Awaitable[tuple[list[dict[str, Any]], str | None]]],
    list[str | None],
]:
    calls: list[str | None] = []
    idx = 0

    async def fetch(page_id: str | None) -> tuple[list[dict[str, Any]], str | None]:
        nonlocal idx
        calls.append(page_id)
        page = pages[idx]
        idx += 1
        return page

    return fetch, calls


async def test_iterate_single_page() -> None:
    fetch, calls = make_fetcher([([{"name": "a"}, {"name": "b"}], None)])
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = [x async for x in it]
    assert [i.name for i in items] == ["a", "b"]
    assert calls == [None]


async def test_iterate_multi_page() -> None:
    fetch, calls = make_fetcher(
        [
            ([{"name": "a"}], "pg2"),
            ([{"name": "b"}], "pg3"),
            ([{"name": "c"}], None),
        ]
    )
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = [x async for x in it]
    assert [i.name for i in items] == ["a", "b", "c"]
    assert calls == [None, "pg2", "pg3"]


async def test_all_collects_into_list() -> None:
    fetch, _ = make_fetcher(
        [([{"name": "a"}], "pg2"), ([{"name": "b"}], None)]
    )
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = await it.all()
    assert [i.name for i in items] == ["a", "b"]


async def test_empty_first_page_terminates() -> None:
    fetch, calls = make_fetcher([([], None)])
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = [x async for x in it]
    assert items == []
    assert calls == [None]
```

- [ ] **Step 10.2: Run tests - verify they fail**

```bash
pytest tests/test_paging.py -v
```

Expected: FAIL - module does not exist.

- [ ] **Step 10.3: Implement `_paging.py`**

```python
# src/ibx_nios_sdk/_paging.py
"""AsyncPageIterator - transparent multi-page async iteration over WAPI list responses."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)

Fetcher = Callable[[str | None], Awaitable[tuple[list[dict[str, Any]], str | None]]]


class AsyncPageIterator(Generic[TModel]):
    """Async iterator yielding parsed model instances from a paged WAPI response.

    Callers pass a ``fetch`` coroutine that takes a ``page_id`` (or ``None``
    for the first page) and returns ``(rows, next_page_id)``. Iteration
    terminates when ``next_page_id`` is ``None`` or ``""``.
    """

    def __init__(self, *, fetch: Fetcher, model: type[TModel]) -> None:
        self._fetch = fetch
        self._model = model

    def __aiter__(self) -> AsyncIterator[TModel]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[TModel]:
        page_id: str | None = None
        first = True
        while first or page_id:
            first = False
            rows, page_id = await self._fetch(page_id)
            for row in rows:
                yield self._model.model_validate(row)

    async def all(self) -> list[TModel]:
        """Collect every page into a single list."""
        return [item async for item in self]
```

- [ ] **Step 10.4: Run tests - pass**

```bash
pytest tests/test_paging.py -v
mypy
ruff check src/ tests/
```

Expected: 4 PASSED.

- [ ] **Step 10.5: Commit**

```bash
git add src/ibx_nios_sdk/_paging.py tests/test_paging.py
git commit -m "feat: AsyncPageIterator for transparent multi-page iteration"
```

---

## Task 11: `WapiResource` base - list_page, list, find_one

**Files:**
- Create: `src/ibx_nios_sdk/_resource.py`
- Create: `tests/test_resource.py`

- [ ] **Step 11.1: Write failing tests**

```python
# tests/test_resource.py
"""WapiResource base behavior - list_page, list, find_one."""

from __future__ import annotations

from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict

from ibx_nios_sdk._http import HttpClient
from ibx_nios_sdk._resource import WapiResource
from tests.conftest import json_response, make_http_client


class FakeA(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")
    _ref: str = ""
    name: str | None = None
    ipv4addr: str | None = None
    view_: str | None = None


class RecordAResource(WapiResource[FakeA]):
    _wapi_type = "record:a"
    _model = FakeA
    _default_return_fields = ["name", "ipv4addr", "view"]


def _session_and_list_handler(pages: list[dict[str, Any]]):
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200,
                json=[{"username": "admin"}],
                headers={"Set-Cookie": "ibapauth=x; Path=/"},
            )
        calls.append(request)
        idx = int(request.url.params.get("_page_id", "0") or "0")
        return json_response(pages[idx])

    return handler, calls


async def test_list_page_sends_paging_params() -> None:
    handler, calls = _session_and_list_handler(
        [{"result": [{"name": "a.example.com"}], "next_page_id": ""}]
    )
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        rows, next_id = await resource.list_page(name="a.example.com")
        assert next_id is None
        assert rows[0].name == "a.example.com"
        params = calls[0].url.params
        assert params["_paging"] == "1"
        assert params["_return_as_object"] == "1"
        assert params["_max_results"] == "1000"
        assert params["_return_fields+"] == "name,ipv4addr,view"
        assert params["name"] == "a.example.com"
    finally:
        await client.aclose()


async def test_list_iterates_pages() -> None:
    pages = [
        {"result": [{"name": "a"}, {"name": "b"}], "next_page_id": "1"},
        {"result": [{"name": "c"}], "next_page_id": ""},
    ]
    handler, _ = _session_and_list_handler(pages)
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        names = [r.name async for r in resource.list()]
        assert names == ["a", "b", "c"]
    finally:
        await client.aclose()


async def test_find_one_returns_first_or_none() -> None:
    handler, _ = _session_and_list_handler(
        [{"result": [{"name": "a"}], "next_page_id": ""}]
    )
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        match = await resource.find_one(name="a")
        assert match is not None and match.name == "a"
    finally:
        await client.aclose()


async def test_find_one_no_match() -> None:
    handler, _ = _session_and_list_handler([{"result": [], "next_page_id": ""}])
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        assert await resource.find_one(name="missing") is None
    finally:
        await client.aclose()


async def test_list_filter_operator() -> None:
    handler, calls = _session_and_list_handler(
        [{"result": [], "next_page_id": ""}]
    )
    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        _ = [r async for r in resource.list(name__like="host")]
        assert calls[0].url.params["name~"] == "host"
    finally:
        await client.aclose()
```

- [ ] **Step 11.2: Run tests - verify they fail**

```bash
pytest tests/test_resource.py -v
```

Expected: FAIL - `_resource` module does not exist.

- [ ] **Step 11.3: Implement `_resource.py`**

```python
# src/ibx_nios_sdk/_resource.py
"""Base resource class for NIOS WAPI objects."""

from __future__ import annotations

from typing import Any, ClassVar, Generic, TypeVar

from pydantic import BaseModel

from ibx_nios_sdk._http import HttpClient
from ibx_nios_sdk._paging import AsyncPageIterator
from ibx_nios_sdk._query import build_filter_params, build_return_fields_params

TModel = TypeVar("TModel", bound=BaseModel)


class WapiResource(Generic[TModel]):
    """Base class for a single WAPI object type.

    Subclasses MUST set the three class variables below.
    """

    _wapi_type: ClassVar[str]
    _model: ClassVar[type[BaseModel]]
    _default_return_fields: ClassVar[list[str]]
    _readonly_fields: ClassVar[set[str]] = set()

    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def _path(self) -> str:
        return f"/{self._wapi_type}"

    def _validate_ref(self, ref: str) -> None:
        prefix = f"{self._wapi_type}/"
        if not ref.startswith(prefix):
            raise ValueError(
                f"ref {ref!r} does not match wapi_type {self._wapi_type!r}"
            )

    async def list_page(
        self,
        *,
        page_id: str | None = None,
        max_results: int = 1000,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        **filters: Any,
    ) -> tuple[list[TModel], str | None]:
        """Fetch a single page of results. Returns (rows, next_page_id)."""
        params: dict[str, str] = {
            "_paging": "1",
            "_return_as_object": "1",
            "_max_results": str(max_results),
        }
        params.update(build_filter_params(filters))
        params.update(
            build_return_fields_params(
                model_fields=self._default_return_fields,
                return_fields=return_fields,
                return_fields_plus=return_fields_plus,
            )
        )
        if page_id:
            params["_page_id"] = page_id

        data = await self._client.get(self._path(), params=params)
        body = data or {}
        rows = body.get("result", []) or []
        next_id = body.get("next_page_id") or None
        parsed = [self._model.model_validate(row) for row in rows]
        return parsed, next_id  # type: ignore[return-value]

    def list(
        self,
        *,
        max_results: int = 1000,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        **filters: Any,
    ) -> AsyncPageIterator[TModel]:
        """Auto-paginated async iterator over all matching objects."""

        async def _fetch(page_id: str | None) -> tuple[list[dict[str, Any]], str | None]:
            params: dict[str, str] = {
                "_paging": "1",
                "_return_as_object": "1",
                "_max_results": str(max_results),
            }
            params.update(build_filter_params(filters))
            params.update(
                build_return_fields_params(
                    model_fields=self._default_return_fields,
                    return_fields=return_fields,
                    return_fields_plus=return_fields_plus,
                )
            )
            if page_id:
                params["_page_id"] = page_id
            data = await self._client.get(self._path(), params=params)
            body = data or {}
            return body.get("result", []) or [], body.get("next_page_id") or None

        return AsyncPageIterator(fetch=_fetch, model=self._model)  # type: ignore[arg-type]

    async def find_one(
        self,
        *,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        **filters: Any,
    ) -> TModel | None:
        rows, _ = await self.list_page(
            max_results=1,
            return_fields=return_fields,
            return_fields_plus=return_fields_plus,
            **filters,
        )
        return rows[0] if rows else None
```

- [ ] **Step 11.4: Run tests - pass**

```bash
pytest tests/test_resource.py -v
mypy
ruff check src/ tests/
```

Expected: 5 PASSED.

- [ ] **Step 11.5: Commit**

```bash
git add src/ibx_nios_sdk/_resource.py tests/test_resource.py
git commit -m "feat: WapiResource base with list_page/list/find_one"
```

---

## Task 12: `WapiResource.get / create / update / delete`

**Files:**
- Modify: `src/ibx_nios_sdk/_resource.py`
- Modify: `tests/test_resource.py`

- [ ] **Step 12.1: Append failing tests**

Add to `tests/test_resource.py`:

```python
import pytest

async def test_get_by_ref_uses_ref_path_and_return_fields() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response({"_ref": "record:a/ZG5z:host.example.com/default", "name": "host.example.com"})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/ZG5z:host.example.com/default"
        obj = await resource.get(ref)
        assert obj.name == "host.example.com"
        path = captured[0].url.path
        assert path.endswith(f"/{ref}")
        assert captured[0].url.params["_return_fields+"] == "name,ipv4addr,view"
    finally:
        await client.aclose()


async def test_get_rejects_mismatched_ref() -> None:
    client = make_http_client(lambda r: json_response({}))
    try:
        resource = RecordAResource(client)
        with pytest.raises(ValueError, match="does not match wapi_type"):
            await resource.get("record:aaaa/XYZ:host/default")
    finally:
        await client.aclose()


async def test_create_posts_payload_and_returns_object() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response({"_ref": "record:a/NEW:host/default", "name": "host", "ipv4addr": "1.2.3.4"})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        payload = FakeA(name="host", ipv4addr="1.2.3.4")
        created = await resource.create(payload)
        assert created.name == "host"
        req = captured[0]
        assert req.method == "POST"
        assert req.url.params["_return_as_object"] == "1"
        body = httpx.Request("POST", req.url, content=req.content).content.decode()
        assert '"name":"host"' in body
        assert '"ipv4addr":"1.2.3.4"' in body
        # None fields excluded
        assert '"view"' not in body
    finally:
        await client.aclose()


async def test_update_puts_partial_payload() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response({"_ref": request.url.path.split("/wapi/v2.14")[-1].lstrip("/"), "name": "host"})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        updated = await resource.update(ref, {"comment": "new comment"})
        assert updated.name == "host"
        req = captured[0]
        assert req.method == "PUT"
        assert req.url.path.endswith(f"/{ref}")
    finally:
        await client.aclose()


async def test_delete_returns_ref() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        return json_response("record:a/XYZ:host/default")

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        result = await resource.delete(ref)
        assert result == ref
    finally:
        await client.aclose()
```

- [ ] **Step 12.2: Run tests - verify they fail**

```bash
pytest tests/test_resource.py -v
```

Expected: the 5 new tests FAIL (methods not defined).

- [ ] **Step 12.3: Add methods to `WapiResource`**

Append to `src/ibx_nios_sdk/_resource.py` (inside class `WapiResource`):

```python
    async def get(
        self,
        ref: str,
        *,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
    ) -> TModel:
        self._validate_ref(ref)
        params = build_return_fields_params(
            model_fields=self._default_return_fields,
            return_fields=return_fields,
            return_fields_plus=return_fields_plus,
        )
        data = await self._client.get(f"/{ref}", params=params or None)
        return self._model.model_validate(data or {})  # type: ignore[return-value]

    async def create(
        self,
        obj: BaseModel | dict[str, Any],
        *,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
    ) -> TModel:
        payload = self._dump(obj, exclude_readonly=False)
        params: dict[str, str] = {"_return_as_object": "1"}
        params.update(
            build_return_fields_params(
                model_fields=self._default_return_fields,
                return_fields=return_fields,
                return_fields_plus=return_fields_plus,
            )
        )
        data = await self._client.post(self._path(), params=params, json=payload)
        return self._model.model_validate(data or {})  # type: ignore[return-value]

    async def update(
        self,
        ref: str,
        obj: BaseModel | dict[str, Any],
        *,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
    ) -> TModel:
        self._validate_ref(ref)
        payload = self._dump(obj, exclude_readonly=True)
        params: dict[str, str] = {"_return_as_object": "1"}
        params.update(
            build_return_fields_params(
                model_fields=self._default_return_fields,
                return_fields=return_fields,
                return_fields_plus=return_fields_plus,
            )
        )
        data = await self._client.put(f"/{ref}", params=params, json=payload)
        return self._model.model_validate(data or {})  # type: ignore[return-value]

    async def delete(self, ref: str) -> str:
        self._validate_ref(ref)
        data = await self._client.delete(f"/{ref}")
        if isinstance(data, dict) and "_value" in data:
            return str(data["_value"])
        return ref

    def _dump(
        self, obj: BaseModel | dict[str, Any], *, exclude_readonly: bool
    ) -> dict[str, Any]:
        if isinstance(obj, BaseModel):
            exclude: set[str] = {"ref"}
            if exclude_readonly:
                exclude |= self._readonly_fields
            return obj.model_dump(by_alias=True, exclude_none=True, exclude=exclude)
        # dict passthrough - caller is responsible for shape.
        return {k: v for k, v in obj.items() if v is not None}
```

- [ ] **Step 12.4: Run tests - pass**

```bash
pytest tests/test_resource.py -v
mypy
ruff check src/ tests/
```

Expected: all PASSED.

- [ ] **Step 12.5: Commit**

```bash
git add src/ibx_nios_sdk/_resource.py tests/test_resource.py
git commit -m "feat: WapiResource get/create/update/delete with _ref validation"
```

---

## Task 13: `WapiResource.call_function` and `set_extattrs` helper

**Files:**
- Modify: `src/ibx_nios_sdk/_resource.py`
- Modify: `tests/test_resource.py`

- [ ] **Step 13.1: Append failing tests**

Add to `tests/test_resource.py`:

```python
async def test_call_function_on_ref() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response({"ips": ["10.0.0.1", "10.0.0.2"]})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        result = await resource.call_function(ref, "next_available_ip", num=2)
        assert result == {"ips": ["10.0.0.1", "10.0.0.2"]}
        req = captured[0]
        assert req.method == "POST"
        assert req.url.path.endswith(f"/{ref}")
        assert req.url.params["_function"] == "next_available_ip"
        assert b'"num":2' in req.content
    finally:
        await client.aclose()


async def test_call_function_without_ref() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response({"ok": True})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        result = await resource.call_function(None, "global_helper", foo="bar")
        assert result == {"ok": True}
        req = captured[0]
        assert req.url.path.endswith("/record:a")
        assert req.url.params["_function"] == "global_helper"
    finally:
        await client.aclose()


async def test_set_extattrs_updates_extattrs_field() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        captured.append(request)
        return json_response({"_ref": "record:a/XYZ:host/default", "name": "host"})

    client = make_http_client(handler)
    try:
        resource = RecordAResource(client)
        ref = "record:a/XYZ:host/default"
        await resource.set_extattrs(ref, Site="NYC", Owner="net-eng")
        req = captured[0]
        assert req.method == "PUT"
        body = req.content.decode()
        assert '"extattrs"' in body
        assert '"Site"' in body and '"NYC"' in body
        assert '"Owner"' in body and '"net-eng"' in body
    finally:
        await client.aclose()
```

- [ ] **Step 13.2: Run - verify failures**

```bash
pytest tests/test_resource.py -v
```

Expected: 3 new tests FAIL.

- [ ] **Step 13.3: Add `call_function` and `set_extattrs` to `WapiResource`**

Append to class `WapiResource` in `_resource.py`:

```python
    async def call_function(
        self,
        ref: str | None,
        function: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """POST ?_function=<name> against a ref (or the wapi_type root if ref is None)."""
        if ref is not None:
            self._validate_ref(ref)
            path = f"/{ref}"
        else:
            path = self._path()
        params = {"_function": function}
        body = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._client.post(path, params=params, json=body or None)
        return data or {}

    async def set_extattrs(self, ref: str, **kwargs: Any) -> TModel:
        """Convenience helper: wrap extattr kwargs into the WAPI nested shape and PUT."""
        extattrs = {name: {"value": value} for name, value in kwargs.items()}
        return await self.update(ref, {"extattrs": extattrs})
```

- [ ] **Step 13.4: Run tests - pass**

```bash
pytest tests/test_resource.py -v
mypy
ruff check src/ tests/
```

Expected: all PASSED.

- [ ] **Step 13.5: Commit**

```bash
git add src/ibx_nios_sdk/_resource.py tests/test_resource.py
git commit -m "feat: WapiResource.call_function and set_extattrs helper"
```

---

## Task 14: `NiosClient` entry point + env-var configuration

**Files:**
- Create: `src/ibx_nios_sdk/client.py`
- Modify: `src/ibx_nios_sdk/__init__.py`
- Create: `tests/test_client.py`

- [ ] **Step 14.1: Write failing tests**

```python
# tests/test_client.py
"""NiosClient entry point and env-var configuration."""

from __future__ import annotations

import httpx
import pytest

from ibx_nios_sdk import NiosClient
from ibx_nios_sdk._exceptions import NiosError
from tests.conftest import json_response


async def test_nios_client_is_async_context_manager() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/grid/session"):
            return httpx.Response(
                200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"}
            )
        if request.url.path.endswith("/logout"):
            return json_response({})
        return json_response({})

    transport = httpx.MockTransport(handler)

    async with NiosClient(
        grid_url="https://grid.example.com",
        username="admin",
        password="infoblox",
        _transport=transport,
    ) as client:
        assert client.grid_url == "https://grid.example.com"


async def test_env_vars_populate_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NIOS_GRID_URL", "https://env-grid.example.com")
    monkeypatch.setenv("NIOS_USERNAME", "envadmin")
    monkeypatch.setenv("NIOS_PASSWORD", "envpass")
    monkeypatch.setenv("NIOS_WAPI_VERSION", "2.12")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{}], headers={"Set-Cookie": "ibapauth=x; Path=/"})

    transport = httpx.MockTransport(handler)
    client = NiosClient(_transport=transport)
    try:
        assert client.grid_url == "https://env-grid.example.com"
        assert client._http._wapi_version == "2.12"
        assert client._http._username == "envadmin"
    finally:
        await client.aclose()


async def test_missing_credentials_raises() -> None:
    with pytest.raises(NiosError, match="credentials"):
        NiosClient(grid_url="https://g.example.com")
```

- [ ] **Step 14.2: Run tests - verify they fail**

```bash
pytest tests/test_client.py -v
```

Expected: FAIL - `NiosClient` not exported yet.

- [ ] **Step 14.3: Implement `client.py`**

```python
# src/ibx_nios_sdk/client.py
"""NiosClient - top-level entry point for the SDK."""

from __future__ import annotations

import os
from pathlib import Path
from types import TracebackType
from typing import Any

import httpx

from ibx_nios_sdk._exceptions import NiosError
from ibx_nios_sdk._http import HttpClient
from ibx_nios_sdk._version import DEFAULT_WAPI_VERSION


class NiosClient:
    """Entry point for the Infoblox NIOS SDK.

    Per-domain services (``dns``, ``dhcp``, ``ipam``, ...) are attached as
    ``@cached_property`` attributes in their respective phase implementations.
    This base class provides HTTP/auth configuration, async-context-manager
    lifecycle, and env-var fallbacks.
    """

    def __init__(
        self,
        *,
        grid_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        wapi_version: str | None = None,
        use_session: bool = True,
        verify: bool | str | Path = True,
        ca_bundle: str | Path | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        _transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        grid_url = grid_url or os.environ.get("NIOS_GRID_URL")
        username = username or os.environ.get("NIOS_USERNAME")
        password = password or os.environ.get("NIOS_PASSWORD")
        wapi_version = wapi_version or os.environ.get("NIOS_WAPI_VERSION") or DEFAULT_WAPI_VERSION

        if not grid_url:
            raise NiosError(message="grid_url is required (set arg or NIOS_GRID_URL env var)")
        if not username or not password:
            raise NiosError(
                message="credentials are required (pass username/password or set NIOS_USERNAME/NIOS_PASSWORD)"
            )

        if ca_bundle is not None:
            verify = str(ca_bundle)

        self._http = HttpClient(
            grid_url=grid_url,
            username=username,
            password=password,
            wapi_version=wapi_version,
            use_session=use_session,
            verify=verify,
            timeout=timeout,
            max_retries=max_retries,
            transport=_transport,
        )

    @property
    def grid_url(self) -> str:
        return self._http.grid_url

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> NiosClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()
```

- [ ] **Step 14.4: Update `src/ibx_nios_sdk/__init__.py`**

```python
"""ibx-nios-sdk - async Python client for Infoblox NIOS WAPI."""

from __future__ import annotations

from ibx_nios_sdk._exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NiosConnectionError,
    NiosError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from ibx_nios_sdk._version import __version__
from ibx_nios_sdk.client import NiosClient

__all__ = [
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "NiosClient",
    "NiosConnectionError",
    "NiosError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ValidationError",
    "__version__",
]
```

- [ ] **Step 14.5: Run tests - pass**

```bash
pytest tests/ -v
mypy
ruff check src/ tests/
ruff format --check src/ tests/
```

Expected: all PASSED (full test suite), mypy/ruff/format all clean.

- [ ] **Step 14.6: Commit**

```bash
git add src/ibx_nios_sdk/__init__.py src/ibx_nios_sdk/client.py tests/test_client.py
git commit -m "feat: NiosClient entry point with env-var configuration"
```

---

## Task 15: CI workflow + CLAUDE.md

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `CLAUDE.md`

- [ ] **Step 15.1: Write `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check src/ tests/
      - run: ruff format --check src/ tests/
      - run: mypy
      - run: pytest -v --cov=ibx_nios_sdk --cov-report=term-missing
```

- [ ] **Step 15.2: Write `CLAUDE.md`**

```markdown
# CLAUDE.md

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate  # Create/activate venv
pip install -e ".[dev]"          # Install with dev deps
pytest -v                        # Run all tests
pytest tests/_http/ -v           # Run a specific directory
pytest -k "test_retry" -v        # Run tests matching pattern
ruff check src/ tests/           # Lint
ruff format src/ tests/          # Format
mypy                             # Type check (strict mode)
```

## Architecture

Async-only SDK built on httpx + pydantic v2. Python 3.11+.

```
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
- **Create/Update** - accept Model or dict. Model serialized with `model_dump(exclude_none=True, by_alias=True, exclude={"ref"} | _readonly_fields)`. WAPI PUT is merge-patch (partial bodies accepted).
- **Function calls** - `await resource.call_function(ref, "next_available_ip", num=5)`. Typed wrappers for common functions live on specific resource subclasses.
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

## Code Style

- Line length: 99 (ruff)
- Ruff rules: E, F, I, UP, B, SIM, TCH
- Private modules prefixed with `_` (e.g. `_http.py`, `_resource.py`)
- Public exports only in `__init__.py`
```

- [ ] **Step 15.3: Final full-suite pass**

```bash
pytest -v
mypy
ruff check src/ tests/
ruff format --check src/ tests/
```

Expected: everything clean.

- [ ] **Step 15.4: Commit**

```bash
git add .github/workflows/ci.yml CLAUDE.md
git commit -m "chore: add CI workflow and CLAUDE.md"
```

---

## Verification Checklist

Before declaring Phase 0+1 complete, confirm:

- [ ] `pip install -e ".[dev]"` from a clean venv succeeds.
- [ ] `pytest -v` shows all tests passing.
- [ ] `mypy` exits clean.
- [ ] `ruff check src/ tests/` exits clean.
- [ ] `ruff format --check src/ tests/` exits clean.
- [ ] `from ibx_nios_sdk import NiosClient, NiosError` works at a Python prompt.
- [ ] Manual smoke: `async with NiosClient(grid_url=..., username=..., password=...) as c: pass` connects, logs in, and logs out cleanly against a real NIOS Grid (record this result - it's Phase 1's acceptance gate).
- [ ] Git log is clean: one commit per task, each message starts with `feat:`, `chore:`, or `fix:`.

## Out of Scope (deferred to later phases)

- Any domain packages (`dns/`, `dhcp/`, etc.) - Phase 2+.
- Typed function wrappers (`network.next_available_ip`) - Phase 3 (IPAM).
- `fileop` multi-step upload flow - Phase 5.
- Zensical docs build - Phase 6.
- Integration tests against a real Grid - Phase 3 onward.
- Migration guide from `infoblox-client` - Phase 6.
