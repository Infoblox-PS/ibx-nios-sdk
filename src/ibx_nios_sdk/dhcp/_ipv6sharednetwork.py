# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6sharednetworkResource - DHCP IPv6 shared network."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6sharednetwork import READONLY_FIELDS, Ipv6sharednetwork


class Ipv6sharednetworkResource(WapiResource[Ipv6sharednetwork]):
    """Manage NIOS DHCPv6 shared network objects."""

    _wapi_type = "ipv6sharednetwork"
    _model = Ipv6sharednetwork
    _default_return_fields = ["name", "network_view", "networks", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"network_view"}
