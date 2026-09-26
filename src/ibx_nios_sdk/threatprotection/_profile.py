# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionProfileResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatprotection.models.threatprotection_profile import (
    READONLY_FIELDS,
    ThreatprotectionProfile,
)


class ThreatprotectionProfileResource(WapiResource[ThreatprotectionProfile]):
    """Manage NIOS Threat Protection profile objects."""

    _wapi_type = "threatprotection:profile"
    _model = ThreatprotectionProfile
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"source_member", "source_profile"}
