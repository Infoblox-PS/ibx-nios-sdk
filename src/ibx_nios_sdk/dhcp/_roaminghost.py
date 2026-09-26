# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RoaminghostResource - DHCP roaming host."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.roaminghost import READONLY_FIELDS, Roaminghost


class RoaminghostResource(WapiResource[Roaminghost]):
    """Manage NIOS DHCP roaming host objects."""

    _wapi_type = "roaminghost"
    _model = Roaminghost
    _default_return_fields = ["name", "mac", "network_view", "address_type", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"ipv6_template", "template"}
