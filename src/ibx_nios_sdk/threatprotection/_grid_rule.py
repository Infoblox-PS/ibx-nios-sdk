# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionGridRuleResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.grid_threatprotection_rule import (
    READONLY_FIELDS,
    ThreatprotectionGridRule,
)


class ThreatprotectionGridRuleResource(WapiResource[ThreatprotectionGridRule]):
    """Manage NIOS Threat Protection Grid-level rule objects."""

    _wapi_type = "threatprotection:grid:rule"
    _model = ThreatprotectionGridRule
    _default_return_fields = ["name", "template", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
