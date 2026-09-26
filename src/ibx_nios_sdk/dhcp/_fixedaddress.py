# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FixedaddressResource - DHCP IPv4 fixed address."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.fixedaddress import READONLY_FIELDS, Fixedaddress


class FixedaddressResource(WapiResource[Fixedaddress]):
    """Manage NIOS DHCP fixed address objects."""

    _wapi_type = "fixedaddress"
    _model = Fixedaddress
    _default_return_fields = ["ipv4addr", "mac", "name", "network", "network_view", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"template"}
