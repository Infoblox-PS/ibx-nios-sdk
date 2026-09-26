# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridThreatinsightResource - NIOS Grid threat insight settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_threatinsight import READONLY_FIELDS, GridThreatinsight


class GridThreatinsightResource(WapiResource[GridThreatinsight]):
    """Manage NIOS Grid Threat Insight configurations."""

    _wapi_type = "grid:threatinsight"
    _model = GridThreatinsight
    _default_return_fields = ["name"]
    _readonly_fields = set(READONLY_FIELDS)
