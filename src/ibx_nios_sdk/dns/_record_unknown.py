# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordUnknown resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_unknown import READONLY_FIELDS, RecordUnknown


class RecordUnknownResource(WapiResource[RecordUnknown]):
    """Manage NIOS DNS generic unknown records (raw wire format)."""

    _wapi_type = "record:unknown"
    _model = RecordUnknown
    _default_return_fields = ["name", "record_type", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
