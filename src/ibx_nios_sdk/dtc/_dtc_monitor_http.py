# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorHttpResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor_http import READONLY_FIELDS, DtcMonitorHttp


class DtcMonitorHttpResource(WapiResource[DtcMonitorHttp]):
    """Manage NIOS DTC HTTP health monitor objects."""

    _wapi_type = "dtc:monitor:http"
    _model = DtcMonitorHttp
    _default_return_fields = ["name", "comment", "port", "secure"]
    _readonly_fields = set(READONLY_FIELDS)
