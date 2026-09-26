# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VlanResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.vlan import READONLY_FIELDS, Vlan


class VlanResource(WapiResource[Vlan]):
    """Manage NIOS VLAN objects."""

    _wapi_type = "vlan"
    _model = Vlan
    _default_return_fields = ["id", "name", "parent", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
