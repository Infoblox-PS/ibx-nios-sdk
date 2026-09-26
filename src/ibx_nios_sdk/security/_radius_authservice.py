# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RadiusAuthserviceResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.radius_authservice import READONLY_FIELDS, RadiusAuthservice


class RadiusAuthserviceResource(WapiResource[RadiusAuthservice]):
    """Manage NIOS RADIUS authentication service objects."""

    _wapi_type = "radius:authservice"
    _model = RadiusAuthservice
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
