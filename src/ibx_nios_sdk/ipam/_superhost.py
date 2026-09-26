# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SuperhostResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.superhost import READONLY_FIELDS, Superhost


class SuperhostResource(WapiResource[Superhost]):
    """Manage NIOS IPAM superhost objects."""

    _wapi_type = "superhost"
    _model = Superhost
    _default_return_fields = ["name", "comment", "dhcp_associated_objects"]
    _readonly_fields = set(READONLY_FIELDS)
