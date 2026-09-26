# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SamlAuthserviceResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.saml_authservice import READONLY_FIELDS, SamlAuthservice


class SamlAuthserviceResource(WapiResource[SamlAuthservice]):
    """Manage NIOS SAML authentication service objects."""

    _wapi_type = "saml:authservice"
    _model = SamlAuthservice
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
