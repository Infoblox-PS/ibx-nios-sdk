# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderGlobalResource - NIOS global Smart Folder, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.smartfolder.models.smartfolder_global import (
    READONLY_FIELDS,
    SmartfolderGlobal,
)


class SmartfolderGlobalResource(WapiResource[SmartfolderGlobal]):
    """Manage NIOS global Smart Folder objects."""

    _wapi_type = "smartfolder:global"
    _model = SmartfolderGlobal
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
