# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzAResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_a import READONLY_FIELDS, RecordRpzA


class RecordRpzAResource(WapiResource[RecordRpzA]):
    """Manage NIOS RPZ A record objects."""

    _wapi_type = "record:rpz:a"
    _model = RecordRpzA
    _default_return_fields = ["name", "ipv4addr", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
