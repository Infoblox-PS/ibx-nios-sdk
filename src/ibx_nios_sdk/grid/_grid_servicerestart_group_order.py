# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartGroupOrderResource - NIOS Grid service-restart group order."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_servicerestart_group_order import (
    READONLY_FIELDS,
    GridServicerestartGroupOrder,
)


class GridServicerestartGroupOrderResource(WapiResource[GridServicerestartGroupOrder]):
    """Manage NIOS Grid service-restart group order objects."""

    _wapi_type = "grid:servicerestart:group:order"
    _model = GridServicerestartGroupOrder
    _default_return_fields = ["groups"]
    _readonly_fields = set(READONLY_FIELDS)
