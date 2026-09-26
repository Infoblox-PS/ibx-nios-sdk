# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorIcmpResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor_icmp import READONLY_FIELDS, DtcMonitorIcmp


class DtcMonitorIcmpResource(WapiResource[DtcMonitorIcmp]):
    """Manage NIOS DTC ICMP health monitor objects."""

    _wapi_type = "dtc:monitor:icmp"
    _model = DtcMonitorIcmp
    _default_return_fields = ["name", "comment", "interval", "timeout"]
    _readonly_fields = set(READONLY_FIELDS)
