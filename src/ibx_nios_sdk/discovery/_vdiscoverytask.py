# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""VdiscoverytaskResource - NIOS virtual discovery task, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.vdiscoverytask import READONLY_FIELDS, Vdiscoverytask


class VdiscoverytaskResource(WapiResource[Vdiscoverytask]):
    """Manage NIOS vDiscovery task objects."""

    _wapi_type = "vdiscoverytask"
    _model = Vdiscoverytask
    _default_return_fields = ["name", "driver_type", "enabled", "state"]
    _readonly_fields = set(READONLY_FIELDS)
