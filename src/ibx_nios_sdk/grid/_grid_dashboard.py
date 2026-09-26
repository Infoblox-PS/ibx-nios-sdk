# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridDashboardResource - NIOS Grid dashboard thresholds."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_dashboard import READONLY_FIELDS, GridDashboard


class GridDashboardResource(WapiResource[GridDashboard]):
    """Access NIOS Grid dashboard statistics (read-only)."""

    _wapi_type = "grid:dashboard"
    _model = GridDashboard
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
