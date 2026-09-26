# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordA resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecord_a import READONLY_FIELDS, SharedrecordA


class SharedrecordAResource(WapiResource[SharedrecordA]):
    """Manage NIOS shared DNS A records (IPv4 address mappings shared across zones)."""

    _wapi_type = "sharedrecord:a"
    _model = SharedrecordA
    _default_return_fields = ["name", "ipv4addr", "shared_record_group", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
