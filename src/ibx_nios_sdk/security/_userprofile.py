# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""UserprofileResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.userprofile import READONLY_FIELDS, Userprofile


class UserprofileResource(WapiResource[Userprofile]):
    """Access NIOS user profile (read-only, returns the current admin's profile)."""

    _wapi_type = "userprofile"
    _model = Userprofile
    _default_return_fields = ["name", "admin_group"]
    _readonly_fields = set(READONLY_FIELDS)
