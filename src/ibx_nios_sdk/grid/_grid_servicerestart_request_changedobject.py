# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartRequestChangedobjectResource - NIOS Grid service-restart changed object."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_servicerestart_request_changedobject import (
    READONLY_FIELDS,
    GridServicerestartRequestChangedobject,
)


class GridServicerestartRequestChangedobjectResource(
    WapiResource[GridServicerestartRequestChangedobject]
):
    """Manage NIOS Grid service restart changed object records."""

    _wapi_type = "grid:servicerestart:request:changedobject"
    _model = GridServicerestartRequestChangedobject
    _default_return_fields = ["object_name", "object_type", "action", "user_name"]
    _readonly_fields = set(READONLY_FIELDS)
