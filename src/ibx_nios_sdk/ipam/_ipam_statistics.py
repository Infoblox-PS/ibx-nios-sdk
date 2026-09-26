# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""IpamStatisticsResource - full implementation.

Note: _wapi_type uses a colon: ``ipam:statistics``.
The IpamService accessor is named ``ipam_statistics``.

NOTE: IpamStatistics is a read-only aggregate view in practice; WAPI will
reject write attempts. No SDK enforcement.
"""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.ipam_statistics import READONLY_FIELDS, IpamStatistics


class IpamStatisticsResource(WapiResource[IpamStatistics]):
    """Access NIOS IPAM statistics (read-only aggregate view)."""

    _wapi_type = "ipam:statistics"
    _model = IpamStatistics
    _default_return_fields = ["network", "network_view", "utilization"]
    _readonly_fields = set(READONLY_FIELDS)
