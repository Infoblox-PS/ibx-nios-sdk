# Contributing

Thanks for your interest in ibx-nios-sdk. This page covers how to get set up,
what the checks expect, and the conventions the codebase follows.

## Getting set up

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,cli,docs]"
```

## The checks

Everything below must pass before a pull request is merged; CI runs the same
commands on Python 3.11, 3.12 and 3.13.

```bash
ruff check .            # lint, whole repo
ruff format --check .   # formatting
mypy                    # strict type check
pytest -q               # unit tests, no grid needed
```

Documentation:

```bash
zensical build          # build the site into site/
pipx run pymarkdownlnt --config pyproject.toml scan -r -e 'docs/superpowers/**' README.md docs/
```

`docs/superpowers/` holds dated design records and is excluded from the
Markdown lint; treat those files as history rather than editing them.

## Live tests

`tests/integration/` talks to a real grid and creates and deletes objects, so
point it at a lab, never production. Copy `.env.example` to `.env` (git-ignored)
and fill in the grid settings:

```bash
cp .env.example .env
NIOS_LIVE=1 pytest tests/integration/ -v
```

Never commit a grid address or credential.

## Conventions

- **Licence header.** Every `.py` file starts with
  `# SPDX-License-Identifier: Apache-2.0` and a copyright line;
  `tests/test_license_headers.py` enforces it.
- **Line length** is 99 for code. Private modules are prefixed with `_`, and
  only `__init__.py` exports public names.
- **Models follow the wire, not the schema.** NIOS sometimes returns a shape
  its own `?_schema` does not declare. `tests/test_schema_conformance.py`
  compares every model field against a snapshot taken from a real grid;
  confirmed exceptions belong in `WIRE_OVERRIDES` in `tests/wapi_schema.py`
  with a note on the evidence.
- **Restrictions are generated, not hand-written.** Refresh the snapshot with
  `tools/refresh_wapi_schema_snapshot.py`, then regenerate the table with
  `tools/refresh_object_restrictions.py`.
- **Tests are async** (`asyncio_mode = "auto"`) and mock HTTP with
  `httpx.MockTransport`; handlers are plain `def`.
- **Commits** describe one concern each, in the imperative mood, with the
  reasoning in the body where it is not obvious from the diff.

## Cutting a release

Releases are driven entirely by an annotated tag; never publish by hand.

1. Bump `version` in `pyproject.toml` and `src/ibx_nios_sdk/_version.py`, the
   README badge, and the assertion in `tests/test_imports.py`.
2. Add the version's section to `CHANGELOG.md`.
3. Commit, then tag with an annotation - its text becomes the GitHub release
   notes:

   ```bash
   git tag -a v1.2.3 -m "v1.2.3 - summary of the release"
   git push origin main v1.2.3
   ```

The tag push runs `release.yml`, which refuses to continue unless the tag
matches the packaged version and the changelog has a matching section, then
builds the wheel and sdist, creates the GitHub release, and publishes to PyPI.

Never move or delete a published tag: GitHub demotes that tag's release to a
draft, and PyPI refuses to accept a version number twice.

## Reporting bugs

Open an issue with the SDK version, the NIOS and WAPI versions, the call you
made, and the full error. `IB_LOG_LEVEL=DEBUG` logs the request and response.
Redact grid addresses, credentials and object references before posting.

For anything security-sensitive, see [SECURITY.md](SECURITY.md) instead.
