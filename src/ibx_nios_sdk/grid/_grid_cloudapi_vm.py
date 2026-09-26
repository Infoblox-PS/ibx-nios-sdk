# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridCloudapiVmResource - NIOS Grid Cloud API VM."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_cloudapi_vm import READONLY_FIELDS, GridCloudapiVm


class GridCloudapiVmResource(WapiResource[GridCloudapiVm]):
    """Manage NIOS Grid Cloud API virtual machine objects."""

    _wapi_type = "grid:cloudapi:vm"
    _model = GridCloudapiVm
    _default_return_fields = ["name", "comment", "hostname", "id"]
    _readonly_fields = set(READONLY_FIELDS)
