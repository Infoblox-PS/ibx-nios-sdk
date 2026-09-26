# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""UpgradestatusResource - NIOS upgrade status (read-only)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.upgradestatus import READONLY_FIELDS, Upgradestatus


class UpgradestatusResource(WapiResource[Upgradestatus]):
    """Access NIOS upgrade status objects (read-only)."""

    _wapi_type = "upgradestatus"
    _model = Upgradestatus
    _default_return_fields = ["member", "current_version", "upgrade_state", "grid_state"]
    _readonly_fields = set(READONLY_FIELDS)
