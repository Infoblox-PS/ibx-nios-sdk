# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6rangetemplateResource - DHCP IPv6 range template."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6rangetemplate import READONLY_FIELDS, Ipv6rangetemplate


class Ipv6rangetemplateResource(WapiResource[Ipv6rangetemplate]):
    """Manage NIOS DHCPv6 range template objects."""

    _wapi_type = "ipv6rangetemplate"
    _model = Ipv6rangetemplate
    _default_return_fields = ["name", "number_of_addresses", "offset", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
