# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""OrderedrangesResource - DHCP ordered ranges aggregate."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.orderedranges import READONLY_FIELDS, Orderedranges


class OrderedrangesResource(WapiResource[Orderedranges]):
    """Manage NIOS DHCP ordered ranges objects."""

    _wapi_type = "orderedranges"
    _model = Orderedranges
    _default_return_fields = ["network", "ranges"]
    _readonly_fields = set(READONLY_FIELDS)
