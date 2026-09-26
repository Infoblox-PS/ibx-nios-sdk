# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SmartfolderPersonalResource - NIOS personal Smart Folder, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.smartfolder.models.smartfolder_personal import (
    READONLY_FIELDS,
    SmartfolderPersonal,
)


class SmartfolderPersonalResource(WapiResource[SmartfolderPersonal]):
    """Manage NIOS personal Smart Folder objects."""

    _wapi_type = "smartfolder:personal"
    _model = SmartfolderPersonal
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
