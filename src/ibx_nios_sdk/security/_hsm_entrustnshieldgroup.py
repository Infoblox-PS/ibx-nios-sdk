# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HsmEntrustnshieldgroupResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.hsm_entrustnshieldgroup import (
    READONLY_FIELDS,
    HsmEntrustnshieldgroup,
)


class HsmEntrustnshieldgroupResource(WapiResource[HsmEntrustnshieldgroup]):
    """Manage NIOS HSM Entrust nShield group objects."""

    _wapi_type = "hsm:entrustnshieldgroup"
    _model = HsmEntrustnshieldgroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
