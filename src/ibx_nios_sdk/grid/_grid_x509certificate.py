# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridX509certificateResource - NIOS Grid X.509 certificate."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.grid_x509certificate import READONLY_FIELDS, GridX509certificate


class GridX509certificateResource(WapiResource[GridX509certificate]):
    """Manage NIOS Grid X.509 certificate objects."""

    _wapi_type = "grid:x509certificate"
    _model = GridX509certificate
    _default_return_fields = ["subject", "issuer", "serial", "valid_not_before", "valid_not_after"]
    _readonly_fields = set(READONLY_FIELDS)
