# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdminroleResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.adminrole import READONLY_FIELDS, Adminrole


class AdminroleResource(WapiResource[Adminrole]):
    """Manage NIOS admin role objects."""

    _wapi_type = "adminrole"
    _model = Adminrole
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
