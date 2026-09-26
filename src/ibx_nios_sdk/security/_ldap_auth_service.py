# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LdapAuthServiceResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.ldap_auth_service import READONLY_FIELDS, LdapAuthService


class LdapAuthServiceResource(WapiResource[LdapAuthService]):
    """Manage NIOS LDAP authentication service objects."""

    _wapi_type = "ldap_auth_service"
    _model = LdapAuthService
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
