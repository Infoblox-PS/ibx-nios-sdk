# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartRequestResource - NIOS Grid service-restart request."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_servicerestart_request import (
    READONLY_FIELDS,
    GridServicerestartRequest,
)


class GridServicerestartRequestResource(WapiResource[GridServicerestartRequest]):
    """Manage NIOS Grid service restart request objects."""

    _wapi_type = "grid:servicerestart:request"
    _model = GridServicerestartRequest
    _default_return_fields = ["member", "service", "state", "result"]
    _readonly_fields = set(READONLY_FIELDS)
