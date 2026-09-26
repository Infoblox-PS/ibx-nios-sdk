# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordAaaa resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecord_aaaa import READONLY_FIELDS, SharedrecordAaaa


class SharedrecordAaaaResource(WapiResource[SharedrecordAaaa]):
    """Manage NIOS shared DNS AAAA records (IPv6 address mappings shared across zones)."""

    _wapi_type = "sharedrecord:aaaa"
    _model = SharedrecordAaaa
    _default_return_fields = ["name", "ipv6addr", "shared_record_group", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
