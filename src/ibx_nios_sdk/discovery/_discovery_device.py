# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceResource - NIOS discovered network device, read-mostly."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_device import READONLY_FIELDS, DiscoveryDevice


class DiscoveryDeviceResource(WapiResource[DiscoveryDevice]):
    """Access NIOS network discovery device records (read-only)."""

    _wapi_type = "discovery:device"
    _model = DiscoveryDevice
    _default_return_fields = ["name", "address", "type"]
    _readonly_fields = set(READONLY_FIELDS)
