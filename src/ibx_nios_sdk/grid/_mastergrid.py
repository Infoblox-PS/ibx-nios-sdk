# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MastergridResource - NIOS Master Grid (GMC) settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.mastergrid import READONLY_FIELDS, Mastergrid


class MastergridResource(WapiResource[Mastergrid]):
    """Manage NIOS master grid configuration objects."""

    _wapi_type = "mastergrid"
    _model = Mastergrid
    _default_return_fields = ["address", "enable", "join_status"]
    _readonly_fields = set(READONLY_FIELDS)
