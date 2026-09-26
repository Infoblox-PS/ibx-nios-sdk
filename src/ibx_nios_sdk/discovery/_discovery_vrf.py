# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryVrfResource - NIOS discovery VRF, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_vrf import READONLY_FIELDS, DiscoveryVrf


class DiscoveryVrfResource(WapiResource[DiscoveryVrf]):
    """Manage NIOS network discovery VRF objects."""

    _wapi_type = "discovery:vrf"
    _model = DiscoveryVrf
    _default_return_fields = ["name", "network_view", "device"]
    _readonly_fields = set(READONLY_FIELDS)
