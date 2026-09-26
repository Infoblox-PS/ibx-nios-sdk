# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiCloudstatisticsResource - NIOS Grid Cloud API statistics."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_cloudapi_cloudstatistics import (
    READONLY_FIELDS,
    GridCloudapiCloudstatistics,
)


class GridCloudapiCloudstatisticsResource(WapiResource[GridCloudapiCloudstatistics]):
    """Access NIOS Grid Cloud API statistics (read-only)."""

    _wapi_type = "grid:cloudapi:cloudstatistics"
    _model = GridCloudapiCloudstatistics
    _default_return_fields = ["allocated_ip_count", "available_ip_count", "tenant_count"]
    _readonly_fields = set(READONLY_FIELDS)
