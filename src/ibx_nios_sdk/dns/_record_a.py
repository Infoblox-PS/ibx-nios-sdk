# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordA resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_a import READONLY_FIELDS, RecordA


class RecordAResource(WapiResource[RecordA]):
    """Manage NIOS DNS A records (name to IPv4 address mappings)."""

    _wapi_type = "record:a"
    _model = RecordA
    _default_return_fields = ["name", "ipv4addr", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
