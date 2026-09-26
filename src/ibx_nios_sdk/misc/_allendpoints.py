# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AllendpointsResource - NIOS allendpoints read-only aggregate."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.allendpoints import READONLY_FIELDS, Allendpoints


class AllendpointsResource(WapiResource[Allendpoints]):
    """Access NIOS all-endpoint aggregate records (read-only)."""

    _wapi_type = "allendpoints"
    _model = Allendpoints
    _default_return_fields = ["comment", "type", "address"]
    _readonly_fields = set(READONLY_FIELDS)
