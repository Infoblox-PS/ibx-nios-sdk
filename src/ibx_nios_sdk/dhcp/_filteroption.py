# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FilteroptionResource - DHCP option filter."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.filteroption import READONLY_FIELDS, Filteroption


class FilteroptionResource(WapiResource[Filteroption]):
    """Manage NIOS DHCP option filter objects."""

    _wapi_type = "filteroption"
    _model = Filteroption
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
