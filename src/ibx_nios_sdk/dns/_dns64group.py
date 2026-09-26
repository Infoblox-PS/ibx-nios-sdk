# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Dns64group resource - DNS64 group CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.dns64group import READONLY_FIELDS, Dns64group


class Dns64groupResource(WapiResource[Dns64group]):
    """Manage NIOS DNS64 synthesis group configurations."""

    _wapi_type = "dns64group"
    _model = Dns64group
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
