# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoverytaskResource - full implementation.

Note: _wapi_type uses a colon: ``discovery:discoverytask``.
The IpamService accessor is named ``discovery_discoverytask``.
"""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.discoverytask import READONLY_FIELDS, Discoverytask


class DiscoverytaskResource(WapiResource[Discoverytask]):
    """Manage NIOS network discovery tasks."""

    _wapi_type = "discoverytask"
    _model = Discoverytask
    _default_return_fields = ["status", "network_view", "member_name"]
    _readonly_fields = set(READONLY_FIELDS)
