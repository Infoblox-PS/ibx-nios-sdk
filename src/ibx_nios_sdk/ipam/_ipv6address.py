# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6addressResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.ipv6address import READONLY_FIELDS, Ipv6address


class Ipv6addressResource(WapiResource[Ipv6address]):
    """Manage NIOS IPAM IPv6 address objects."""

    _wapi_type = "ipv6address"
    _model = Ipv6address
    _default_return_fields = ["ip_address", "duid", "network", "network_view", "usage"]
    _readonly_fields = set(READONLY_FIELDS)
