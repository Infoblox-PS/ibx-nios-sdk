# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridDnsResource - NIOS Grid DNS properties."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_dns import READONLY_FIELDS, GridDns


class GridDnsResource(WapiResource[GridDns]):
    """Manage NIOS Grid-level DNS property configurations."""

    _wapi_type = "grid:dns"
    _model = GridDns
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
