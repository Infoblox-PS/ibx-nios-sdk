# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AuthpolicyResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.authpolicy import READONLY_FIELDS, Authpolicy


class AuthpolicyResource(WapiResource[Authpolicy]):
    """Manage NIOS authentication policy objects."""

    _wapi_type = "authpolicy"
    _model = Authpolicy
    _default_return_fields = ["auth_services", "default_group"]
    _readonly_fields = set(READONLY_FIELDS)
