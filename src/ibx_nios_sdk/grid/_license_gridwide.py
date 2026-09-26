# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LicenseGridwideResource - NIOS grid-wide license."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.license_gridwide import READONLY_FIELDS, LicenseGridwide


class LicenseGridwideResource(WapiResource[LicenseGridwide]):
    """Manage NIOS grid-wide license objects."""

    _wapi_type = "license:gridwide"
    _model = LicenseGridwide
    _default_return_fields = ["type", "key", "limit", "expiration_status"]
    _readonly_fields = set(READONLY_FIELDS)
