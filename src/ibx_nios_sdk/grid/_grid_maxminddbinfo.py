# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridMaxminddbinfoResource - NIOS Grid MaxMind DB info."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_maxminddbinfo import READONLY_FIELDS, GridMaxminddbinfo


class GridMaxminddbinfoResource(WapiResource[GridMaxminddbinfo]):
    """Access NIOS Grid MaxMind database information (read-only)."""

    _wapi_type = "grid:maxminddbinfo"
    _model = GridMaxminddbinfo
    _default_return_fields = ["member", "database_type", "topology_type", "deployment_time"]
    _readonly_fields = set(READONLY_FIELDS)
