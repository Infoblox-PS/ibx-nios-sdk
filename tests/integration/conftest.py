# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Load grid settings for the live suite from a git-ignored ``.env``.

The live tests read ``NIOS_GRID_URL``, ``NIOS_USERNAME`` and ``NIOS_PASSWORD``
(plus the optional ``NIOS_WAPI_VERSION`` and ``NIOS_VERIFY``). Keeping them in
``.env`` at the repository root means no grid address or credential is ever
committed; see ``.env.example`` for the template.

Real environment variables win over ``.env``, so CI and one-off overrides work
without editing the file. When python-dotenv is not installed, a minimal
``KEY=VALUE`` parser is used instead, so the suite needs no new dependency.
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


def _load_without_dotenv(path: Path) -> None:
    """Parse a simple KEY=VALUE file, ignoring blanks, comments and quotes."""
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.removeprefix("export ").strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env_file() -> None:
    # Only for live runs: a plain unit-test run must not inherit grid settings
    # from .env, or tests that assert on an unset NIOS_* variable would fail.
    if not os.getenv("NIOS_LIVE") or not ENV_FILE.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        _load_without_dotenv(ENV_FILE)
        return
    load_dotenv(ENV_FILE, override=False)


_load_env_file()
