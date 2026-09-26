# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NatgroupResource - NIOS NAT group."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.natgroup import READONLY_FIELDS, Natgroup


class NatgroupResource(WapiResource[Natgroup]):
    """Manage NIOS NAT group objects."""

    _wapi_type = "natgroup"
    _model = Natgroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
