# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryMemberpropertiesResource - NIOS discovery member properties."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_memberproperties import (
    READONLY_FIELDS,
    DiscoveryMemberproperties,
)


class DiscoveryMemberpropertiesResource(WapiResource[DiscoveryMemberproperties]):
    """Manage NIOS network discovery member-level property objects."""

    _wapi_type = "discovery:memberproperties"
    _model = DiscoveryMemberproperties
    _default_return_fields = ["discovery_member", "address", "role"]
    _readonly_fields = set(READONLY_FIELDS)
