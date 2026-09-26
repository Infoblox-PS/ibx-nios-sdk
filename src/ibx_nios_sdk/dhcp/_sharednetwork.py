# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharednetworkResource - DHCP IPv4 shared network."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.sharednetwork import READONLY_FIELDS, Sharednetwork


class SharednetworkResource(WapiResource[Sharednetwork]):
    """Manage NIOS DHCP shared network objects."""

    _wapi_type = "sharednetwork"
    _model = Sharednetwork
    _default_return_fields = ["name", "network_view", "networks", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"network_view"}
