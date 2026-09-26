# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AdAuthServiceResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.ad_auth_service import READONLY_FIELDS, AdAuthService


class AdAuthServiceResource(WapiResource[AdAuthService]):
    """Manage NIOS Active Directory authentication service objects."""

    _wapi_type = "ad_auth_service"
    _model = AdAuthService
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
