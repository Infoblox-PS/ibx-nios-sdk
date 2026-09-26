# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpoptiondefinitionResource - DHCP option definition."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.dhcpoptiondefinition import READONLY_FIELDS, Dhcpoptiondefinition


class DhcpoptiondefinitionResource(WapiResource[Dhcpoptiondefinition]):
    """Manage NIOS DHCP option definition objects."""

    _wapi_type = "dhcpoptiondefinition"
    _model = Dhcpoptiondefinition
    _default_return_fields = ["name", "code", "space", "type"]
    _readonly_fields = set(READONLY_FIELDS)
