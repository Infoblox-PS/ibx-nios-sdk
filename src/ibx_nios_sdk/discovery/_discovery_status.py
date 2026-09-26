# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryStatusResource - NIOS discovery status, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_status import READONLY_FIELDS, DiscoveryStatus


class DiscoveryStatusResource(WapiResource[DiscoveryStatus]):
    """Access NIOS network discovery status records (read-only)."""

    _wapi_type = "discovery:status"
    _model = DiscoveryStatus
    _default_return_fields = ["address", "status", "type"]
    _readonly_fields = set(READONLY_FIELDS)
