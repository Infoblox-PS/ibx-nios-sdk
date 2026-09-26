# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordAaaa resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_aaaa import READONLY_FIELDS, RecordAaaa


class RecordAaaaResource(WapiResource[RecordAaaa]):
    """Manage NIOS DNS AAAA records (name to IPv6 address mappings)."""

    _wapi_type = "record:aaaa"
    _model = RecordAaaa
    _default_return_fields = ["name", "ipv6addr", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
