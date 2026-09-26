# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdminuserResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.adminuser import READONLY_FIELDS, Adminuser


class AdminuserResource(WapiResource[Adminuser]):
    """Manage NIOS admin user objects."""

    _wapi_type = "adminuser"
    _model = Adminuser
    _default_return_fields = ["name", "comment", "admin_groups"]
    _readonly_fields = set(READONLY_FIELDS)
