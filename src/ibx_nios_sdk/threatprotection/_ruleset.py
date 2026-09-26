# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRulesetResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_ruleset import (
    READONLY_FIELDS,
    ThreatprotectionRuleset,
)


class ThreatprotectionRulesetResource(WapiResource[ThreatprotectionRuleset]):
    """Manage NIOS Threat Protection rule set objects."""

    _wapi_type = "threatprotection:ruleset"
    _model = ThreatprotectionRuleset
    _default_return_fields = ["version", "used_by", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
