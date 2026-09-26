# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpoptionspaceResource - DHCP option space."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.dhcpoptionspace import READONLY_FIELDS, Dhcpoptionspace


class DhcpoptionspaceResource(WapiResource[Dhcpoptionspace]):
    """Manage NIOS DHCP option space objects."""

    _wapi_type = "dhcpoptionspace"
    _model = Dhcpoptionspace
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
