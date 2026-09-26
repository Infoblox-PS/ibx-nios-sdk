# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv4addressResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.ipv4address import READONLY_FIELDS, Ipv4address


class Ipv4addressResource(WapiResource[Ipv4address]):
    """Manage NIOS IPAM IPv4 address objects."""

    _wapi_type = "ipv4address"
    _model = Ipv4address
    _default_return_fields = ["ip_address", "mac_address", "network", "network_view", "usage"]
    _readonly_fields = set(READONLY_FIELDS)
