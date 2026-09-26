# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MacfilteraddressResource - DHCP MAC filter address."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.macfilteraddress import READONLY_FIELDS, Macfilteraddress


class MacfilteraddressResource(WapiResource[Macfilteraddress]):
    """Manage NIOS DHCP MAC filter address objects."""

    _wapi_type = "macfilteraddress"
    _model = Macfilteraddress
    _default_return_fields = ["mac", "filter", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
