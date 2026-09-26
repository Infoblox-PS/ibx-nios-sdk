# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridLicensePoolResource - NIOS Grid license pool."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_license_pool import READONLY_FIELDS, GridLicensePool


class GridLicensePoolResource(WapiResource[GridLicensePool]):
    """Manage NIOS Grid license pool objects."""

    _wapi_type = "grid:license_pool"
    _model = GridLicensePool
    _default_return_fields = ["type", "key", "limit", "installed", "assigned"]
    _readonly_fields = set(READONLY_FIELDS)
