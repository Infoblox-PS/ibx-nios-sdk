# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworkuserResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.networkuser import READONLY_FIELDS, Networkuser


class NetworkuserResource(WapiResource[Networkuser]):
    """Manage NIOS network user objects."""

    _wapi_type = "networkuser"
    _model = Networkuser
    _default_return_fields = ["name", "address", "user_status"]
    _readonly_fields = set(READONLY_FIELDS)
