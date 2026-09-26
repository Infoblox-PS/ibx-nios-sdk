# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiVmaddressResource - NIOS Grid Cloud API VM address."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_cloudapi_vmaddress import (
    READONLY_FIELDS,
    GridCloudapiVmaddress,
)


class GridCloudapiVmaddressResource(WapiResource[GridCloudapiVmaddress]):
    """Manage NIOS Grid Cloud API VM address objects."""

    _wapi_type = "grid:cloudapi:vmaddress"
    _model = GridCloudapiVmaddress
    _default_return_fields = ["vm_id", "vm_name", "address", "vm_hostname"]
    _readonly_fields = set(READONLY_FIELDS)
