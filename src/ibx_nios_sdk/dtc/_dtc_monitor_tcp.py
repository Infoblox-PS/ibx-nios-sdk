# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorTcpResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor_tcp import READONLY_FIELDS, DtcMonitorTcp


class DtcMonitorTcpResource(WapiResource[DtcMonitorTcp]):
    """Manage NIOS DTC TCP health monitor objects."""

    _wapi_type = "dtc:monitor:tcp"
    _model = DtcMonitorTcp
    _default_return_fields = ["name", "comment", "port"]
    _readonly_fields = set(READONLY_FIELDS)
