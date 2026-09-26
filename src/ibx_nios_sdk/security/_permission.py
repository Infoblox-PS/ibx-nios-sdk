# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""PermissionResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.permission import READONLY_FIELDS, Permission


class PermissionResource(WapiResource[Permission]):
    """Manage NIOS permission objects."""

    _wapi_type = "permission"
    _model = Permission
    _default_return_fields = ["permission", "resource_type", "group"]
    _readonly_fields = set(READONLY_FIELDS)
