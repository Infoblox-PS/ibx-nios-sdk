# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FingerprintResource - DHCP fingerprint."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.fingerprint import READONLY_FIELDS, Fingerprint


class FingerprintResource(WapiResource[Fingerprint]):
    """Manage NIOS DHCP fingerprint objects."""

    _wapi_type = "fingerprint"
    _model = Fingerprint
    _default_return_fields = ["name", "comment", "type", "device_class"]
    _readonly_fields = set(READONLY_FIELDS)
