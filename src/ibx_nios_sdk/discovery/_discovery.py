# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryResource - NIOS discovery object, GET and PUT."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery import READONLY_FIELDS, Discovery


class DiscoveryResource(WapiResource[Discovery]):
    """Manage NIOS network discovery global configuration objects."""

    _wapi_type = "discovery"
    _model = Discovery
    _default_return_fields = []
    _readonly_fields = set(READONLY_FIELDS)
