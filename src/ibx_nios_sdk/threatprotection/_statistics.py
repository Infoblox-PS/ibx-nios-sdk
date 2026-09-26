# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionStatisticsResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_statistics import (
    READONLY_FIELDS,
    ThreatprotectionStatistics,
)


class ThreatprotectionStatisticsResource(WapiResource[ThreatprotectionStatistics]):
    """Access NIOS Threat Protection statistics (read-only aggregate)."""

    _wapi_type = "threatprotection:statistics"
    _model = ThreatprotectionStatistics
    _default_return_fields = ["member", "stat_infos"]
    _readonly_fields = set(READONLY_FIELDS)
