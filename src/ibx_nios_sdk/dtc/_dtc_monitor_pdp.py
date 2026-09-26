# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcMonitorPdpResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_monitor_pdp import READONLY_FIELDS, DtcMonitorPdp


class DtcMonitorPdpResource(WapiResource[DtcMonitorPdp]):
    """Manage NIOS DTC PDP health monitor objects."""

    _wapi_type = "dtc:monitor:pdp"
    _model = DtcMonitorPdp
    _default_return_fields = ["name", "comment", "port"]
    _readonly_fields = set(READONLY_FIELDS)
