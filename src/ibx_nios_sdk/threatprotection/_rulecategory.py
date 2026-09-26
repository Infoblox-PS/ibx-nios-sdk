# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionRulecategoryResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_rulecategory import (
    READONLY_FIELDS,
    ThreatprotectionRulecategory,
)


class ThreatprotectionRulecategoryResource(WapiResource[ThreatprotectionRulecategory]):
    """Manage NIOS Threat Protection rule category objects."""

    _wapi_type = "threatprotection:rulecategory"
    _model = ThreatprotectionRulecategory
    _default_return_fields = ["name", "ruleset"]
    _readonly_fields = set(READONLY_FIELDS)
