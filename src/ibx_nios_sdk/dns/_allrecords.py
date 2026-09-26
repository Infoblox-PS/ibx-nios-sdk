# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Allrecords resource - read-only aggregate DNS record list."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.allrecords import READONLY_FIELDS, Allrecords


class AllrecordsResource(WapiResource[Allrecords]):
    """Manage NIOS DNS allrecords objects (read-only aggregate record list)."""

    _wapi_type = "allrecords"
    _model = Allrecords
    _default_return_fields = ["name", "type", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
