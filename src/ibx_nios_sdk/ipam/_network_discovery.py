# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkDiscoveryResource - full implementation.

NOTE: NetworkDiscovery is a read-only aggregate view in practice; WAPI will
reject write attempts. No SDK enforcement.
"""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.network_discovery import READONLY_FIELDS, NetworkDiscovery


class NetworkDiscoveryResource(WapiResource[NetworkDiscovery]):
    """Access NIOS network discovery results (read-only aggregate view)."""

    _wapi_type = "network_discovery"
    _model = NetworkDiscovery
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
