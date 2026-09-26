# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VlanviewResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.vlanview import READONLY_FIELDS, Vlanview


class VlanviewResource(WapiResource[Vlanview]):
    """Manage NIOS VLAN view objects."""

    _wapi_type = "vlanview"
    _model = Vlanview
    _default_return_fields = ["name", "start_vlan_id", "end_vlan_id", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
