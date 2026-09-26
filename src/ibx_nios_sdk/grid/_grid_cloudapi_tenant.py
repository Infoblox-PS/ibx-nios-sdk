# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiTenantResource - NIOS Grid Cloud API tenant."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_cloudapi_tenant import READONLY_FIELDS, GridCloudapiTenant


class GridCloudapiTenantResource(WapiResource[GridCloudapiTenant]):
    """Manage NIOS Grid Cloud API tenant objects."""

    _wapi_type = "grid:cloudapi:tenant"
    _model = GridCloudapiTenant
    _default_return_fields = ["name", "comment", "id"]
    _readonly_fields = set(READONLY_FIELDS)
