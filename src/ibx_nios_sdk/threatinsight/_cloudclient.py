# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightCloudclientResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.threatinsight.models.threatinsight_cloudclient import (
    READONLY_FIELDS,
    ThreatinsightCloudclient,
)


class ThreatinsightCloudclientResource(WapiResource[ThreatinsightCloudclient]):
    """Manage NIOS Threat Insight cloud client configuration objects."""

    _wapi_type = "threatinsight:cloudclient"
    _model = ThreatinsightCloudclient
    _default_return_fields = ["enable"]
    _readonly_fields = set(READONLY_FIELDS)
