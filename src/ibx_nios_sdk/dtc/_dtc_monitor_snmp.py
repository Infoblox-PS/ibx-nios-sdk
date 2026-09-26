# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorSnmpResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor_snmp import READONLY_FIELDS, DtcMonitorSnmp


class DtcMonitorSnmpResource(WapiResource[DtcMonitorSnmp]):
    """Manage NIOS DTC SNMP health monitor objects."""

    _wapi_type = "dtc:monitor:snmp"
    _model = DtcMonitorSnmp
    _default_return_fields = ["name", "comment", "community", "version"]
    _readonly_fields = set(READONLY_FIELDS)
