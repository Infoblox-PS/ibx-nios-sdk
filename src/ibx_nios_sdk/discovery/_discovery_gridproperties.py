# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryGridpropertiesResource - NIOS discovery grid properties."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_gridproperties import (
    READONLY_FIELDS,
    DiscoveryGridproperties,
)


class DiscoveryGridpropertiesResource(WapiResource[DiscoveryGridproperties]):
    """Manage NIOS network discovery grid-level property objects."""

    _wapi_type = "discovery:gridproperties"
    _model = DiscoveryGridproperties
    _default_return_fields = ["grid_name"]
    _readonly_fields = set(READONLY_FIELDS)
