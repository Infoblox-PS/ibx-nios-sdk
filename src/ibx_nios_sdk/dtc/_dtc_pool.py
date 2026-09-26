# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcPoolResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_pool import READONLY_FIELDS, DtcPool


class DtcPoolResource(WapiResource[DtcPool]):
    """Manage NIOS DTC server pool objects."""

    _wapi_type = "dtc:pool"
    _model = DtcPool
    _default_return_fields = ["name", "comment", "availability", "lb_preferred_method"]
    _readonly_fields = set(READONLY_FIELDS)
