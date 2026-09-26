# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""PxgridEndpointResource - NIOS pxGrid endpoint, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.pxgrid_endpoint import READONLY_FIELDS, PxgridEndpoint


class PxgridEndpointResource(WapiResource[PxgridEndpoint]):
    """Manage NIOS pxGrid endpoint objects."""

    _wapi_type = "pxgrid:endpoint"
    _model = PxgridEndpoint
    _default_return_fields = ["name", "comment", "disable", "address"]
    _readonly_fields = set(READONLY_FIELDS)
