# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartStatusResource - NIOS Grid service-restart status."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_servicerestart_status import (
    READONLY_FIELDS,
    GridServicerestartStatus,
)


class GridServicerestartStatusResource(WapiResource[GridServicerestartStatus]):
    """Access NIOS Grid service restart status objects (read-only)."""

    _wapi_type = "grid:servicerestart:status"
    _model = GridServicerestartStatus
    _default_return_fields = ["parent", "pending", "success", "failures"]
    _readonly_fields = set(READONLY_FIELDS)
