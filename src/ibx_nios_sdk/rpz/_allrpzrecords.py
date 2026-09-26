# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AllrpzrecordsResource - read-only aggregate, full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.allrpzrecords import READONLY_FIELDS, Allrpzrecords


class AllrpzrecordsResource(WapiResource[Allrpzrecords]):
    """Access NIOS RPZ records (read-only aggregate - list/get only)."""

    _wapi_type = "allrpzrecords"
    _model = Allrpzrecords
    _default_return_fields = ["name", "type", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
