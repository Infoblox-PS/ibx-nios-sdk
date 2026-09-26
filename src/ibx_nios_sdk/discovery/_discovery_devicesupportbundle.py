# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevicesupportbundleResource - NIOS discovery device support bundle."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.discovery.models.discovery_devicesupportbundle import (
    READONLY_FIELDS,
    DiscoveryDevicesupportbundle,
)


class DiscoveryDevicesupportbundleResource(WapiResource[DiscoveryDevicesupportbundle]):
    """Manage NIOS network discovery device support bundle objects."""

    _wapi_type = "discovery:devicesupportbundle"
    _model = DiscoveryDevicesupportbundle
    _default_return_fields = ["name", "version", "author"]
    _readonly_fields = set(READONLY_FIELDS)
