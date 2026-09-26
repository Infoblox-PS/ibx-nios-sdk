# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridDhcppropertiesResource - NIOS Grid DHCP properties."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_dhcpproperties import READONLY_FIELDS, GridDhcpproperties


class GridDhcppropertiesResource(WapiResource[GridDhcpproperties]):
    """Manage NIOS Grid-level DHCP property configurations."""

    _wapi_type = "grid:dhcpproperties"
    _model = GridDhcpproperties
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
