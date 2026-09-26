# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberDhcppropertiesResource - NIOS member DHCP properties."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_dhcpproperties import READONLY_FIELDS, MemberDhcpproperties


class MemberDhcppropertiesResource(WapiResource[MemberDhcpproperties]):
    """Manage NIOS member-level DHCP property configurations."""

    _wapi_type = "member:dhcpproperties"
    _model = MemberDhcpproperties
    _default_return_fields = ["host_name", "ipv4addr"]
    _readonly_fields = set(READONLY_FIELDS)
