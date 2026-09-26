# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridMemberCloudapiResource - NIOS per-member Cloud API settings.

NOTE: WAPI type is ``grid:member:cloudapi``.
"""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_member_cloudapi import READONLY_FIELDS, GridMemberCloudapi


class GridMemberCloudapiResource(WapiResource[GridMemberCloudapi]):
    """Manage NIOS Grid member Cloud API configurations."""

    _wapi_type = "grid:member:cloudapi"
    _model = GridMemberCloudapi
    _default_return_fields = ["member", "enable_service", "status"]
    _readonly_fields = set(READONLY_FIELDS)
