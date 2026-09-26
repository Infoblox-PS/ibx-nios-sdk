# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevicecomponentResource - NIOS discovered device component, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_devicecomponent import (
    READONLY_FIELDS,
    DiscoveryDevicecomponent,
)


class DiscoveryDevicecomponentResource(WapiResource[DiscoveryDevicecomponent]):
    """Access NIOS network discovery device component records (read-only)."""

    _wapi_type = "discovery:devicecomponent"
    _model = DiscoveryDevicecomponent
    _default_return_fields = ["component_name", "device", "type"]
    _readonly_fields = set(READONLY_FIELDS)
