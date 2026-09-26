# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""UpgradescheduleResource - NIOS upgrade schedule."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.upgradeschedule import READONLY_FIELDS, Upgradeschedule


class UpgradescheduleResource(WapiResource[Upgradeschedule]):
    """Manage NIOS upgrade schedule objects."""

    _wapi_type = "upgradeschedule"
    _model = Upgradeschedule
    _default_return_fields = ["active", "start_time"]
    _readonly_fields = set(READONLY_FIELDS)
