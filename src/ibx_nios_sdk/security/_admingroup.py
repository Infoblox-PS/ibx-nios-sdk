# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdmingroupResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.admingroup import READONLY_FIELDS, Admingroup


class AdmingroupResource(WapiResource[Admingroup]):
    """Manage NIOS admin group objects."""

    _wapi_type = "admingroup"
    _model = Admingroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
