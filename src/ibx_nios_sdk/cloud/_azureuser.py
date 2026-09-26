# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""AzureuserResource - NIOS Azure user, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.cloud.models.azureuser import READONLY_FIELDS, Azureuser


class AzureuserResource(WapiResource[Azureuser]):
    """Manage NIOS Azure user credentials objects."""

    _wapi_type = "azureuser"
    _model = Azureuser
    _default_return_fields = ["name"]
    _readonly_fields = set(READONLY_FIELDS)
