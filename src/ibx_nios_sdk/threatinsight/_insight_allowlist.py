# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightInsightAllowlistResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatinsight.models.threatinsight_insight_allowlist import (
    READONLY_FIELDS,
    ThreatinsightInsightAllowlist,
)


class ThreatinsightInsightAllowlistResource(WapiResource[ThreatinsightInsightAllowlist]):
    """Manage NIOS Threat Insight per-insight allowlist objects."""

    _wapi_type = "threatinsight:insight_allowlist"
    _model = ThreatinsightInsightAllowlist
    _default_return_fields = ["version"]
    _readonly_fields = set(READONLY_FIELDS)
