# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridThreatprotectionResource - NIOS Grid threat protection settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_threatprotection import READONLY_FIELDS, GridThreatprotection


class GridThreatprotectionResource(WapiResource[GridThreatprotection]):
    """Manage NIOS Grid Threat Protection configurations."""

    _wapi_type = "grid:threatprotection"
    _model = GridThreatprotection
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
