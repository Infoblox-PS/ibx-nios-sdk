# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRuletemplateResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_ruletemplate import (
    READONLY_FIELDS,
    ThreatprotectionRuletemplate,
)


class ThreatprotectionRuletemplateResource(WapiResource[ThreatprotectionRuletemplate]):
    """Manage NIOS Threat Protection rule template objects."""

    _wapi_type = "threatprotection:ruletemplate"
    _model = ThreatprotectionRuletemplate
    _default_return_fields = ["name", "category", "ruleset", "description"]
    _readonly_fields = set(READONLY_FIELDS)
