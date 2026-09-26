# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridLicensePoolContainerResource - NIOS Grid license pool container."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_license_pool_container import (
    READONLY_FIELDS,
    GridLicensePoolContainer,
)


class GridLicensePoolContainerResource(WapiResource[GridLicensePoolContainer]):
    """Manage NIOS Grid license pool container objects."""

    _wapi_type = "grid:license_pool_container"
    _model = GridLicensePoolContainer
    _default_return_fields = ["lpc_uid", "last_entitlement_update"]
    _readonly_fields = set(READONLY_FIELDS)
