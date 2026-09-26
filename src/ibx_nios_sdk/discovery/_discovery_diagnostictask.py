# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDiagnostictaskResource - NIOS discovery diagnostic task."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_diagnostictask import (
    READONLY_FIELDS,
    DiscoveryDiagnostictask,
)


class DiscoveryDiagnostictaskResource(WapiResource[DiscoveryDiagnostictask]):
    """Manage NIOS network discovery diagnostic task objects."""

    _wapi_type = "discovery:diagnostictask"
    _model = DiscoveryDiagnostictask
    _default_return_fields = ["ip_address", "network_view", "task_id"]
    _readonly_fields = set(READONLY_FIELDS)
