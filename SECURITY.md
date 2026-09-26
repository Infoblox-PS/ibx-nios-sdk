# Security Policy

## Supported versions

Fixes land on the latest release. Older releases are not patched.

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |

## Reporting a vulnerability

Do not open a public issue for a security problem.

Report it through GitHub's private vulnerability reporting on this repository
(Security -> Report a vulnerability), which notifies the maintainers without
disclosing the details publicly.

Please include what you found, how to reproduce it, and the versions involved.
Redact grid addresses, credentials and object references.

For a vulnerability in NIOS itself rather than in this SDK, contact Infoblox
Support through your usual channel; this repository covers the client library
only.

## Handling credentials

The SDK reads `NIOS_GRID_URL`, `NIOS_USERNAME` and `NIOS_PASSWORD` from the
environment so credentials stay out of source. A few notes on using it safely:

- TLS verification is on by default. Prefer `ca_bundle=` with your grid's CA
  over `verify=False`, which disables certificate checking entirely and is
  meant for throwaway labs.
- `IB_LOG_LEVEL=DEBUG` logs full requests and responses, including headers.
  Do not enable it in production or paste its output into an issue unredacted.
- Session mode holds an `ibapauth` cookie for the life of the client and calls
  `/logout` on close. Use the context manager so the session is always closed.
- `NiosClient.read_raw()` rejects credential-bearing query parameter names, but
  it is still a raw pass-through: prefer the typed resource APIs.
- Never commit a `.env`; it is git-ignored for this reason.
