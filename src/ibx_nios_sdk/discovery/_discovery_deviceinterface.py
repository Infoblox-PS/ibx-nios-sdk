# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceinterfaceResource - NIOS discovered device interface."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_deviceinterface import (
    READONLY_FIELDS,
    DiscoveryDeviceinterface,
)


class DiscoveryDeviceinterfaceResource(WapiResource[DiscoveryDeviceinterface]):
    """Access NIOS network discovery device interface records (read-only)."""

    _wapi_type = "discovery:deviceinterface"
    _model = DiscoveryDeviceinterface
    _default_return_fields = ["name", "mac", "type"]
    _readonly_fields = set(READONLY_FIELDS)
