# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6dhcpoptiondefinitionResource - DHCP IPv6 option definition."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6dhcpoptiondefinition import (
    READONLY_FIELDS,
    Ipv6dhcpoptiondefinition,
)


class Ipv6dhcpoptiondefinitionResource(WapiResource[Ipv6dhcpoptiondefinition]):
    """Manage NIOS DHCPv6 option definition objects."""

    _wapi_type = "ipv6dhcpoptiondefinition"
    _model = Ipv6dhcpoptiondefinition
    _default_return_fields = ["name", "code", "space", "type"]
    _readonly_fields = set(READONLY_FIELDS)
