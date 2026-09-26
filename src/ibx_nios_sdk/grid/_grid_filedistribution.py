# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridFiledistributionResource - NIOS Grid file distribution settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_filedistribution import READONLY_FIELDS, GridFiledistribution


class GridFiledistributionResource(WapiResource[GridFiledistribution]):
    """Manage NIOS Grid file distribution configurations."""

    _wapi_type = "grid:filedistribution"
    _model = GridFiledistribution
    _default_return_fields = ["name"]
    _readonly_fields = set(READONLY_FIELDS)
