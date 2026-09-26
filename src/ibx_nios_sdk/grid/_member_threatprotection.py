# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberThreatprotectionResource - NIOS member threat protection settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_threatprotection import (
    READONLY_FIELDS,
    MemberThreatprotection,
)


class MemberThreatprotectionResource(WapiResource[MemberThreatprotection]):
    """Manage NIOS member Threat Protection configurations."""

    _wapi_type = "member:threatprotection"
    _model = MemberThreatprotection
    _default_return_fields = ["host_name", "comment", "enable_service"]
    _readonly_fields = set(READONLY_FIELDS)
