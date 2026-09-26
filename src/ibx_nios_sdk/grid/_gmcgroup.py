# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GmcgroupResource - NIOS GMC group."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.gmcgroup import READONLY_FIELDS, Gmcgroup


class GmcgroupResource(WapiResource[Gmcgroup]):
    """Manage NIOS Grid member cloud (GMC) group objects."""

    _wapi_type = "gmcgroup"
    _model = Gmcgroup
    _default_return_fields = ["name", "comment", "gmc_promotion_policy"]
    _readonly_fields = set(READONLY_FIELDS)
