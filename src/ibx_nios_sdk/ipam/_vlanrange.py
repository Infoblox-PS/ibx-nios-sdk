# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VlanrangeResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.vlanrange import READONLY_FIELDS, Vlanrange


class VlanrangeResource(WapiResource[Vlanrange]):
    """Manage NIOS VLAN range objects."""

    _wapi_type = "vlanrange"
    _model = Vlanrange
    _default_return_fields = ["name", "vlan_view", "start_vlan_id", "end_vlan_id"]
    _readonly_fields = set(READONLY_FIELDS)
