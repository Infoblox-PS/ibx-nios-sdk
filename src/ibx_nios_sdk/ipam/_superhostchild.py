# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SuperhostchildResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.superhostchild import READONLY_FIELDS, Superhostchild


class SuperhostchildResource(WapiResource[Superhostchild]):
    """Manage NIOS IPAM superhost child objects."""

    _wapi_type = "superhostchild"
    _model = Superhostchild
    _default_return_fields = ["name", "record_parent", "parent"]
    _readonly_fields = set(READONLY_FIELDS)
