# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcResource - global DTC config object, GET+PUT only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc import READONLY_FIELDS, Dtc


class DtcResource(WapiResource[Dtc]):
    """Manage NIOS DTC (Dynamic Traffic Control) global configuration objects."""

    _wapi_type = "dtc"
    _model = Dtc
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
