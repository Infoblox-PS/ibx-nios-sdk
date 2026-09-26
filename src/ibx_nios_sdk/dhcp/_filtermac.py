# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FiltermacResource - DHCP MAC filter."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.filtermac import READONLY_FIELDS, Filtermac


class FiltermacResource(WapiResource[Filtermac]):
    """Manage NIOS DHCP MAC address filter objects."""

    _wapi_type = "filtermac"
    _model = Filtermac
    _default_return_fields = ["name", "comment", "lease_time"]
    _readonly_fields = set(READONLY_FIELDS)
