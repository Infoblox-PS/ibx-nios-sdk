# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorSipResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor_sip import READONLY_FIELDS, DtcMonitorSip


class DtcMonitorSipResource(WapiResource[DtcMonitorSip]):
    """Manage NIOS DTC SIP health monitor objects."""

    _wapi_type = "dtc:monitor:sip"
    _model = DtcMonitorSip
    _default_return_fields = ["name", "comment", "port", "transport"]
    _readonly_fields = set(READONLY_FIELDS)
