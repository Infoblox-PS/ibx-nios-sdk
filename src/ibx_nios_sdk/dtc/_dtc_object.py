# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcObjectResource - GET+PUT (no POST/DELETE)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_object import READONLY_FIELDS, DtcObject


class DtcObjectResource(WapiResource[DtcObject]):
    """Access NIOS DTC object records (read-only aggregate)."""

    _wapi_type = "dtc:object"
    _model = DtcObject
    _default_return_fields = ["name", "comment", "display_type", "status"]
    _readonly_fields = set(READONLY_FIELDS)
