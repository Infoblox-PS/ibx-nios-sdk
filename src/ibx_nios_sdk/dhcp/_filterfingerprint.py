# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FilterfingerprintResource - DHCP fingerprint filter."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.filterfingerprint import READONLY_FIELDS, Filterfingerprint


class FilterfingerprintResource(WapiResource[Filterfingerprint]):
    """Manage NIOS DHCP fingerprint filter objects."""

    _wapi_type = "filterfingerprint"
    _model = Filterfingerprint
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
