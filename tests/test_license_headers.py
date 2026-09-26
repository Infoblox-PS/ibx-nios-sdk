# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Every tracked Python file must carry the SPDX licence header.

The SDK is distributed under Apache-2.0. A file that loses its header is
still covered by the root ``LICENSE``, but the notice is what travels with the
file when someone copies it out, so it is enforced here.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPDX = "# SPDX-License-Identifier: Apache-2.0"
COPYRIGHT_PREFIX = "# Copyright (C) "


def _tracked_python_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "*.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [ROOT / line for line in result.stdout.split()]


FILES = _tracked_python_files()


def test_repository_has_python_files() -> None:
    """Guard against the git listing silently returning nothing."""
    assert len(FILES) > 500


@pytest.mark.parametrize("path", FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_file_declares_its_licence(path: Path) -> None:
    head = path.read_text().split("\n")[:4]
    assert SPDX in head, f"missing {SPDX!r} in the first lines of {path.name}"
    assert any(line.startswith(COPYRIGHT_PREFIX) for line in head), (
        f"missing a copyright line in {path.name}"
    )


def test_licence_file_is_apache2() -> None:
    text = (ROOT / "LICENSE").read_text()
    assert "Apache License" in text
    assert "Version 2.0, January 2004" in text


def test_packaging_metadata_declares_apache2() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text()
    assert 'license = "Apache-2.0"' in pyproject
    assert 'license-files = ["LICENSE"]' in pyproject
