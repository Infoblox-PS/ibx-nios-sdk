# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberLicenseResource - NIOS member license."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_license import READONLY_FIELDS, MemberLicense


class MemberLicenseResource(WapiResource[MemberLicense]):
    """Manage NIOS member license objects."""

    _wapi_type = "member:license"
    _model = MemberLicense
    _default_return_fields = ["hwid", "key", "kind", "type"]
    _readonly_fields = set(READONLY_FIELDS)
