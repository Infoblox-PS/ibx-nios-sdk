# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionProfileRuleResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_profile_rule import (
    READONLY_FIELDS,
    ThreatprotectionProfileRule,
)


class ThreatprotectionProfileRuleResource(WapiResource[ThreatprotectionProfileRule]):
    """Manage NIOS Threat Protection profile rule objects."""

    _wapi_type = "threatprotection:profile:rule"
    _model = ThreatprotectionProfileRule
    _default_return_fields = ["profile", "rule", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
