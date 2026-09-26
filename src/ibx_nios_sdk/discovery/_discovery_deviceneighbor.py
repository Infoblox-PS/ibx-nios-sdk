# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDeviceneighborResource - NIOS discovered device neighbor, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_deviceneighbor import (
    READONLY_FIELDS,
    DiscoveryDeviceneighbor,
)


class DiscoveryDeviceneighborResource(WapiResource[DiscoveryDeviceneighbor]):
    """Access NIOS network discovery device neighbor records (read-only)."""

    _wapi_type = "discovery:deviceneighbor"
    _model = DiscoveryDeviceneighbor
    _default_return_fields = ["name", "address", "device"]
    _readonly_fields = set(READONLY_FIELDS)
