# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberThreatinsightResource - NIOS member threat insight settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_threatinsight import READONLY_FIELDS, MemberThreatinsight


class MemberThreatinsightResource(WapiResource[MemberThreatinsight]):
    """Manage NIOS member Threat Insight configurations."""

    _wapi_type = "member:threatinsight"
    _model = MemberThreatinsight
    _default_return_fields = ["host_name", "enable_service", "status"]
    _readonly_fields = set(READONLY_FIELDS)
