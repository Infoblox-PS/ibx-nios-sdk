# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorResource - GET+PUT (no POST/DELETE)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor import READONLY_FIELDS, DtcMonitor


class DtcMonitorResource(WapiResource[DtcMonitor]):
    """Manage NIOS DTC health monitor objects."""

    _wapi_type = "dtc:monitor"
    _model = DtcMonitor
    _default_return_fields = ["name", "comment", "type"]
    _readonly_fields = set(READONLY_FIELDS)
