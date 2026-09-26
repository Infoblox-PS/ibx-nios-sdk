# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightAllowlistResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatinsight.models.threatinsight_allowlist import (
    READONLY_FIELDS,
    ThreatinsightAllowlist,
)


class ThreatinsightAllowlistResource(WapiResource[ThreatinsightAllowlist]):
    """Manage NIOS Threat Insight allowlist objects."""

    _wapi_type = "threatinsight:allowlist"
    _model = ThreatinsightAllowlist
    _default_return_fields = ["fqdn", "type", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
