# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6fixedaddressResource - DHCP IPv6 fixed address."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6fixedaddress import READONLY_FIELDS, Ipv6fixedaddress


class Ipv6fixedaddressResource(WapiResource[Ipv6fixedaddress]):
    """Manage NIOS DHCPv6 fixed address objects."""

    _wapi_type = "ipv6fixedaddress"
    _model = Ipv6fixedaddress
    _default_return_fields = ["ipv6addr", "duid", "name", "network", "network_view", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"template"}
