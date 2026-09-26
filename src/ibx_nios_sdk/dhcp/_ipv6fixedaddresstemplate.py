# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6fixedaddresstemplateResource - DHCP IPv6 fixed address template."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.ipv6fixedaddresstemplate import (
    READONLY_FIELDS,
    Ipv6fixedaddresstemplate,
)


class Ipv6fixedaddresstemplateResource(WapiResource[Ipv6fixedaddresstemplate]):
    """Manage NIOS DHCPv6 fixed address template objects."""

    _wapi_type = "ipv6fixedaddresstemplate"
    _model = Ipv6fixedaddresstemplate
    _default_return_fields = ["name", "number_of_addresses", "offset", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
