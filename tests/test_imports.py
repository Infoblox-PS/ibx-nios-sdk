# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Smoke tests - verify the package is importable and exposes expected top-level names."""

from __future__ import annotations


def test_package_importable() -> None:
    import ibx_nios_sdk

    assert hasattr(ibx_nios_sdk, "__version__")
    assert ibx_nios_sdk.__version__ == "1.0.0"


def test_default_wapi_version() -> None:
    from ibx_nios_sdk._version import DEFAULT_WAPI_VERSION

    assert DEFAULT_WAPI_VERSION == "2.14"
