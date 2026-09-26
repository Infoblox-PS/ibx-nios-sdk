# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiResource - NIOS Grid Cloud API settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_cloudapi import READONLY_FIELDS, GridCloudapi


class GridCloudapiResource(WapiResource[GridCloudapi]):
    """Manage NIOS Grid Cloud API configuration objects."""

    _wapi_type = "grid:cloudapi"
    _model = GridCloudapi
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
