# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRuleResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_rule import (
    READONLY_FIELDS,
    ThreatprotectionRule,
)


class ThreatprotectionRuleResource(WapiResource[ThreatprotectionRule]):
    """Manage NIOS Threat Protection rule objects."""

    _wapi_type = "threatprotection:rule"
    _model = ThreatprotectionRule
    _default_return_fields = ["disable"]
    _readonly_fields = set(READONLY_FIELDS)
