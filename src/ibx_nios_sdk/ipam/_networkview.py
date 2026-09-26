# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkviewResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.networkview import READONLY_FIELDS, Networkview


class NetworkviewResource(WapiResource[Networkview]):
    """Manage NIOS IPAM network view objects."""

    _wapi_type = "networkview"
    _model = Networkview
    _default_return_fields = ["name", "is_default", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
