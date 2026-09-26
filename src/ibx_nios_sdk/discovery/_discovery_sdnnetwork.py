# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoverySdnnetworkResource - NIOS discovery SDN network, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_sdnnetwork import (
    READONLY_FIELDS,
    DiscoverySdnnetwork,
)


class DiscoverySdnnetworkResource(WapiResource[DiscoverySdnnetwork]):
    """Access NIOS network discovery SDN network records (read-only)."""

    _wapi_type = "discovery:sdnnetwork"
    _model = DiscoverySdnnetwork
    _default_return_fields = ["name", "network_view"]
    _readonly_fields = set(READONLY_FIELDS)
