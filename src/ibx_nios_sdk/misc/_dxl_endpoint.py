# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DxlEndpointResource - NIOS DXL endpoint, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.dxl_endpoint import READONLY_FIELDS, DxlEndpoint


class DxlEndpointResource(WapiResource[DxlEndpoint]):
    """Manage NIOS DXL endpoint objects."""

    _wapi_type = "dxl:endpoint"
    _model = DxlEndpoint
    _default_return_fields = ["name", "comment", "disable", "log_level"]
    _readonly_fields = set(READONLY_FIELDS)
