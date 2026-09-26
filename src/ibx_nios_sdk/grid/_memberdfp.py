# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberdfpResource - NIOS member DFP settings."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.memberdfp import READONLY_FIELDS, Memberdfp


class MemberdfpResource(WapiResource[Memberdfp]):
    """Manage NIOS member DNS Firewall Policy (DFP) configurations."""

    _wapi_type = "memberdfp"
    _model = Memberdfp
    _default_return_fields = ["host_name", "dfp_forward_first", "is_dfp_override"]
    _readonly_fields = set(READONLY_FIELDS)
