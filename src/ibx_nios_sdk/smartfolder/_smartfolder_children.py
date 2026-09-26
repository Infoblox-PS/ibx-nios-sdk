# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderChildrenResource - NIOS Smart Folder children, GET only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.smartfolder.models.smartfolder_children import (
    READONLY_FIELDS,
    SmartfolderChildren,
)


class SmartfolderChildrenResource(WapiResource[SmartfolderChildren]):
    """Access NIOS Smart Folder children records (read-only)."""

    _wapi_type = "smartfolder:children"
    _model = SmartfolderChildren
    _default_return_fields = ["resource", "value_type"]
    _readonly_fields = set(READONLY_FIELDS)
