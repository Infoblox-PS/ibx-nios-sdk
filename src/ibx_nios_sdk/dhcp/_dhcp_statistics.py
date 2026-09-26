# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpStatisticsResource - DHCP statistics (read-only aggregate).

Note: _wapi_type uses a colon: ``dhcp:statistics``.
The DhcpService accessor is named ``dhcp_statistics``.
"""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.dhcp_statistics import READONLY_FIELDS, DhcpStatistics


class DhcpStatisticsResource(WapiResource[DhcpStatistics]):
    """Access NIOS DHCP statistics (read-only aggregate view)."""

    _wapi_type = "dhcp:statistics"
    _model = DhcpStatistics
    _default_return_fields = ["dhcp_utilization"]
    _readonly_fields = set(READONLY_FIELDS)
