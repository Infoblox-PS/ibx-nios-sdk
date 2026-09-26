# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDhcid resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_dhcid import READONLY_FIELDS, RecordDhcid


class RecordDhcidResource(WapiResource[RecordDhcid]):
    """Manage NIOS DNS DHCID records (DHCP client identifiers)."""

    _wapi_type = "record:dhcid"
    _model = RecordDhcid
    _default_return_fields = ["name", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
