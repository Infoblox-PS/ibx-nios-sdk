# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FilternacResource - DHCP NAC filter."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.filternac import READONLY_FIELDS, Filternac


class FilternacResource(WapiResource[Filternac]):
    """Manage NIOS DHCP NAC filter objects."""

    _wapi_type = "filternac"
    _model = Filternac
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
