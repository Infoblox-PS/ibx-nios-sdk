# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-26

First public release.

### Added

- Async client for the Infoblox NIOS WAPI, covering 17 domains and 280 object
  types with a hand-written pydantic v2 model per type.
- Session-cookie authentication by default, with a single re-login and retry on
  a 401, and HTTP Basic per request as an alternative.
- Auto-paginated `list()` returning an async iterator, plus `list_page()` for
  single-page control, `find_one()`, and `get()` by `_ref`.
- Filter operators through keyword suffixes: `name__like`, `name__gte`,
  `name__lte`, `name__not`, and `extattr_<Name>` for extensible attributes.
- Per-object-type operation restrictions. WAPI refuses operations an object type
  does not support; the SDK raises `UnsupportedOperationError` before the
  request rather than letting the grid answer. `call_function()` is never gated,
  and `NiosClient(enforce_restrictions=False)` opts out.
- Typed wrappers for common WAPI functions (`next_available_ip`,
  `next_available_network`, `restart_services`, and others), with a generic
  `call_function()` for the rest.
- Ten `nios-*` command line utilities in the `cli` extra, and 22 worked example
  scripts under `docs/examples/`.
- Exponential-backoff retry on 429, 502, 503 and 504; 500 is not retried,
  because WAPI returns it for legitimate validation errors.
- TLS verification on by default, with `ca_bundle=` for a private CA and clear
  errors when verification fails.
- Documentation at <https://infoblox-ps.github.io/ibx-nios-sdk/>, including a
  guide per domain, common patterns, troubleshooting, and the full API
  reference.

[1.0.0]: https://github.com/Infoblox-PS/ibx-nios-sdk/releases/tag/v1.0.0
