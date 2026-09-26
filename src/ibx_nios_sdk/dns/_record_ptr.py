# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordPtr resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_ptr import READONLY_FIELDS, RecordPtr


class RecordPtrResource(WapiResource[RecordPtr]):
    """Manage NIOS DNS PTR records (reverse pointer records from IP to name)."""

    _wapi_type = "record:ptr"
    _model = RecordPtr
    _default_return_fields = [
        "ptrdname",
        "ipv4addr",
        "ipv6addr",
        "name",
        "view",
        "zone",
        "comment",
    ]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
