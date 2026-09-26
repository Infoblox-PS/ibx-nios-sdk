# ibx-nios-sdk

[![CI](https://github.com/Infoblox-PS/ibx-nios-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/Infoblox-PS/ibx-nios-sdk/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/Infoblox-PS/ibx-nios-sdk)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/Infoblox-PS/ibx-nios-sdk)
[![Typed](https://img.shields.io/badge/type--checked-mypy%20strict-blue.svg)](http://mypy-lang.org/)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-orange.svg)](https://docs.astral.sh/ruff/)
[![Docs](https://img.shields.io/badge/docs-infoblox--ps.github.io-00BD4D.svg)](https://infoblox-ps.github.io/ibx-nios-sdk/)

Async Python SDK for Infoblox NIOS WAPI. Built on [httpx](https://www.python-httpx.org/) and [pydantic v2](https://docs.pydantic.dev/), with full type safety and IDE autocomplete. Aligned with **WAPI v2.14**. Requires Python 3.11+.

**📖 Documentation: <https://infoblox-ps.github.io/ibx-nios-sdk/>** - guides for every
WAPI domain, common patterns, the CLI utilities, 22 worked examples, and the full
API reference. Start with
[Getting Started](https://infoblox-ps.github.io/ibx-nios-sdk/getting-started/),
[Common Patterns](https://infoblox-ps.github.io/ibx-nios-sdk/common-patterns/), or the
[API Reference](https://infoblox-ps.github.io/ibx-nios-sdk/reference/).

## Installation

Base SDK (library only):

```bash
pip install ibx-nios-sdk
```

### Optional extras

The package ships three optional dependency groups. Combine them in a single
bracketed list as needed.

| Extra  | Pulls in                                      | Install when you want to…                                         |
|--------|-----------------------------------------------|-------------------------------------------------------------------|
| `cli`  | `click`, `click-option-group`                 | use the `nios-csvexport`, `nios-grid-backup`, … console scripts   |
| `docs` | `zensical`                                    | build the documentation site locally                              |
| `dev`  | `pytest`, `pytest-asyncio`, `mypy`, `ruff`, … | run the test suite, lint, and type-check                          |

```bash
pip install 'ibx-nios-sdk[cli]'                 # library + CLI tools
pip install 'ibx-nios-sdk[cli,docs]'            # + docs builder
pip install 'ibx-nios-sdk[cli,dev,docs]'        # everything
```

### Installing from a local sdist

When installing from a downloaded `.tar.gz`, let the shell expand `~` and quote
only the extras brackets (so zsh doesn't try to glob them):

```bash
pip install ~/Downloads/ibx_nios_sdk-0.1.1.tar.gz'[cli]'
```

### Using `uv`

Inside a project checkout:

```bash
uv sync                                         # base deps
uv sync --extra cli
uv sync --extra cli --extra dev --extra docs
uv sync --all-extras                            # shortcut for all three
```

As a dependency in another project:

```bash
uv add 'ibx-nios-sdk[cli]'
```

### About the docs

The `docs` extra installs the **tool** that builds the documentation
(`zensical`), not the rendered site. The Markdown sources under `docs/` ship
inside the sdist but are not copied into `site-packages` - to build or browse
the docs locally, clone the repo (or extract the sdist) and run `make docs-serve`.
The canonical reader-facing copy is the hosted site at
<https://infoblox-ps.github.io/ibx-nios-sdk/>, rebuilt from `main` by the Docs
workflow.

## Quick Start

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient(
        grid_url="https://grid.example.com",
        username="admin",
        password="infoblox",
    ) as client:
        async for record in client.dns.record_a.list(zone="example.com"):
            print(record.name, record.ipv4addr)

asyncio.run(main())
```

Every call follows the same pattern: `client.<domain>.<resource>.<operation>()`.

## Configuration

```python
client = NiosClient(
    grid_url="https://grid.example.com",   # or set NIOS_GRID_URL
    username="admin",                      # or NIOS_USERNAME
    password="infoblox",                   # or NIOS_PASSWORD
    wapi_version="2.14",                   # or NIOS_WAPI_VERSION; default "2.14"
    use_session=True,                      # lazy /grid/session login + cookie reuse
    verify=True,                           # TLS verify; pass False or a CA bundle path
    timeout=30.0,                          # seconds
    max_retries=3,                         # 429/5xx retry with exponential backoff
)
```

**Debug logging:** `IB_LOG_LEVEL=DEBUG` prints request URLs, retry attempts, timings.

## Core Patterns

- **Session auth by default.** First request triggers `/grid/session` and a cookie is reused; `/logout` on close. On 401 the SDK re-authenticates once and retries transparently.
- **Retry.** Exponential backoff on 429/502/503/504. 500 is not retried (WAPI returns 500 for legitimate validation errors).
- **Auto-paginated `list()`.** Returns an `AsyncPageIterator` - iterate with `async for`, or call `.all()` for a materialised list. `list_page(max_results=N)` exposes single-page control.
- **Filter operators via kwarg suffix:** `name="x"` exact, `name__like="x"` substring, `name__gte=5`, `name__lte=5`, `name__not="x"`, `extattr_Site="NYC"`.
- **Return fields.** `_return_fields+=<model fields>` is sent by default so the full pydantic model populates. Trim with `return_fields=[…]` or extend with `return_fields_plus=[…]`.
- **Create / Update.** Accept a pydantic Model or a plain dict. Model serialisation honours `_readonly_fields` (stripped on PUT) and `_create_only_fields` (kept on POST, stripped on PUT).
- **Function calls.** `await resource.call_function(ref, "next_available_ip", num=5)`. Typed wrappers exist for common functions. Never blocked by restrictions.
- **Per-type operation restrictions.** WAPI forbids some operations per object type - `allrecords` is a read-only aggregate, `grid` cannot be deleted, and function-only types (`dtc`, `discovery`) refuse even a read. The SDK raises `UnsupportedOperationError` before the request instead of letting the grid answer `Operation <op> not allowed for <type>`. Opt out with `NiosClient(enforce_restrictions=False)`.

## Example: end-to-end DNS

```python
# Create an A record
a = await client.dns.record_a.create({
    "name": "svc1.example.com",
    "ipv4addr": "10.0.0.10",
    "view": "default",
    "comment": "web frontend",
})

# Update (view is create-only; stripped automatically on PUT)
await client.dns.record_a.update(a.ref, {"comment": "web frontend (prod)"})

# Next available IP from a /24
result = await client.ipam.network.call_function(
    "network/ZG5z:10.0.0.0/24/default",
    "next_available_ip",
    num=3,
)

# Delete
await client.dns.record_a.delete(a.ref)
```

## WAPI Version Compatibility

The SDK's pydantic models, readonly / create-only field sets, default return-field lists, and `Literal[...]` enum types are calibrated against **NIOS WAPI v2.14**. The HTTP layer is version-agnostic, so pointing at an older grid (2.10–2.13) does not fail immediately - but expect concrete friction:

- **List / get can return `400 AdmConProtoError: Unknown argument`.** The SDK requests every modelled field via `_return_fields+=…` and older schemas reject names that were added later. Mitigation: pass `return_fields=[…]` explicitly, or subclass the resource and override `_default_return_fields`.
- **Writes may be rejected** if you populate a field the older grid does not know.
- **Newer object types are 404s** on older grids (`parentalcontrol:*`, `record:dtclbdn`, `rir:organization`, …).
- **Per-type operation restrictions are recorded from 2.14.** If an older or newer grid allows an operation this SDK gates (or vice versa), pass `enforce_restrictions=False` and let the grid decide.
- **Reads are tolerant.** All model fields are `Optional`; missing values deserialise as `None`. `Literal[...] | str` unions accept unknown enum values via the `str` fallback.

Recommended practice: pin the SDK release to a line aligned with your grid's WAPI version rather than mixing majors.

## CLI Utilities

10 `nios-*` console entry points are bundled with the `[cli]` extra:

```text
nios-csvexport          nios-csvimport         nios-get-file
nios-get-log            nios-get-supportbundle nios-grid-backup
nios-grid-restore       nios-certificate       nios-restart-service
nios-restart-status
```

Full reference: [`docs/cli-utilities.md`](docs/cli-utilities.md).

## Examples

22 workflow scripts under [`docs/examples/`](docs/examples/). Highlights:

- `manage_dns_records.py` - A / AAAA / CNAME / MX / PTR lifecycle
- `manage_networks.py` - Networks, containers, ranges, sharednetworks
- `manage_next_available_ip.py` - `next_available_ip` / `next_available_network` function-call patterns
- `manage_dtc_full.py` - flagship end-to-end DTC deploy / teardown / status / health / migrate
- `manage_grid.py`, `manage_members.py`, `manage_discovery.py`, `manage_cloud.py`, `manage_fileop.py`, …

See [`docs/examples-index.md`](docs/examples-index.md) for the full index.

## Testing

```bash
pytest -q                              # unit tests (MockTransport, no grid needed)
NIOS_LIVE=1 pytest tests/integration/  # live tests against a real grid
ruff check .                           # lint (whole repo, docs/examples included)
ruff format .                          # format
mypy                                   # strict type check
pytest --cov=ibx_nios_sdk              # coverage report
```

The live suite needs `NIOS_LIVE=1` and a reachable grid. Put the grid settings in
a `.env` at the repository root, which is git-ignored:

```bash
cp .env.example .env     # then fill in NIOS_GRID_URL / NIOS_USERNAME / NIOS_PASSWORD
NIOS_LIVE=1 pytest tests/integration/ -v
```

Real environment variables take precedence over `.env`, so CI and one-off runs can
override any of them. The live tests create and delete real objects: point them at
a lab grid, never production. No grid address or credential belongs in the repo.

## License

Apache License 2.0 - see [LICENSE](LICENSE).

```text
ibx-nios-sdk - async Python client for Infoblox NIOS WAPI
Copyright 2026 Infoblox, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

Every source file carries an SPDX identifier (`Apache-2.0`). Apache-2.0 is
permissive: you can use this SDK inside proprietary or differently licensed
software without that software inheriting the licence. The runtime dependencies
are permissive too: httpx (BSD-3-Clause), pydantic (MIT), python-dateutil
(Apache-2.0/BSD-3-Clause), and - for the `[cli]` extra - click and
click-option-group (BSD-3-Clause).

## Trademarks

INFOBLOX is a trademark of Infoblox Inc. or its affiliated companies, registered in the
United States and other countries. Infoblox Grid is a trademark of Infoblox Inc. Other
Infoblox product names used here, such as NIOS, are used descriptively to identify the
products this SDK operates against and remain the property of their owner. "WAPI" is
used in its plain sense, as the name of the NIOS Web API.
