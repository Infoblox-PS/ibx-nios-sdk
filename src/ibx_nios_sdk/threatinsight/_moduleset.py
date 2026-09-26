# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightModulesetResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatinsight.models.threatinsight_moduleset import (
    READONLY_FIELDS,
    ThreatinsightModuleset,
)


class ThreatinsightModulesetResource(WapiResource[ThreatinsightModuleset]):
    """Manage NIOS Threat Insight module set objects."""

    _wapi_type = "threatinsight:moduleset"
    _model = ThreatinsightModuleset
    _default_return_fields = ["version"]
    _readonly_fields = set(READONLY_FIELDS)
