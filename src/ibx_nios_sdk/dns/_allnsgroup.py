# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Allnsgroup resource (read-only aggregate list)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.allnsgroup import READONLY_FIELDS, Allnsgroup


class AllnsgroupResource(WapiResource[Allnsgroup]):
    """Manage NIOS DNS allnsgroup objects (aggregate name-server group view)."""

    _wapi_type = "allnsgroup"
    _model = Allnsgroup
    _default_return_fields = ["name", "type"]
    _readonly_fields = set(READONLY_FIELDS)
