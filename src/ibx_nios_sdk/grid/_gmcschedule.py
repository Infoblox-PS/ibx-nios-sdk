# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GmcscheduleResource - NIOS GMC schedule."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.gmcschedule import READONLY_FIELDS, Gmcschedule


class GmcscheduleResource(WapiResource[Gmcschedule]):
    """Manage NIOS Grid member cloud (GMC) schedule objects."""

    _wapi_type = "gmcschedule"
    _model = Gmcschedule
    _default_return_fields = ["activate_gmc_group_schedule"]
    _readonly_fields = set(READONLY_FIELDS)
