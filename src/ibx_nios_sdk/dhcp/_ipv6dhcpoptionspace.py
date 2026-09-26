# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6dhcpoptionspaceResource - DHCP IPv6 option space."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6dhcpoptionspace import READONLY_FIELDS, Ipv6dhcpoptionspace


class Ipv6dhcpoptionspaceResource(WapiResource[Ipv6dhcpoptionspace]):
    """Manage NIOS DHCPv6 option space objects."""

    _wapi_type = "ipv6dhcpoptionspace"
    _model = Ipv6dhcpoptionspace
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
