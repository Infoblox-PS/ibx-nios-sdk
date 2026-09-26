# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6filteroptionResource - DHCP IPv6 option filter."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6filteroption import READONLY_FIELDS, Ipv6filteroption


class Ipv6filteroptionResource(WapiResource[Ipv6filteroption]):
    """Manage NIOS DHCPv6 option filter objects."""

    _wapi_type = "ipv6filteroption"
    _model = Ipv6filteroption
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
