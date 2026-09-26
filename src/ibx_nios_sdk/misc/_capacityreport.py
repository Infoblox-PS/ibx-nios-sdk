# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CapacityreportResource - NIOS capacity report, read-only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.capacityreport import READONLY_FIELDS, Capacityreport


class CapacityreportResource(WapiResource[Capacityreport]):
    """Access NIOS capacity report records (read-only aggregate)."""

    _wapi_type = "capacityreport"
    _model = Capacityreport
    _default_return_fields = ["name", "hardware_type", "percent_used", "total_objects"]
    _readonly_fields = set(READONLY_FIELDS)
