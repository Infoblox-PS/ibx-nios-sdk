# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneAuthDiscrepancy resource - read-only zone auth discrepancy list."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_auth_discrepancy import (
    READONLY_FIELDS,
    ZoneAuthDiscrepancy,
)


class ZoneAuthDiscrepancyResource(WapiResource[ZoneAuthDiscrepancy]):
    """Manage NIOS authoritative zone discrepancy reports."""

    _wapi_type = "zone_auth_discrepancy"
    _model = ZoneAuthDiscrepancy
    _default_return_fields = ["zone", "description", "severity", "timestamp"]
    _readonly_fields = set(READONLY_FIELDS)
