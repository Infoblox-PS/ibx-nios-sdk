# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""UpgradegroupResource - NIOS upgrade group."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.upgradegroup import READONLY_FIELDS, Upgradegroup


class UpgradegroupResource(WapiResource[Upgradegroup]):
    """Manage NIOS upgrade group objects."""

    _wapi_type = "upgradegroup"
    _model = Upgradegroup
    _default_return_fields = ["name", "comment", "upgrade_policy", "distribution_policy"]
    _readonly_fields = set(READONLY_FIELDS)
