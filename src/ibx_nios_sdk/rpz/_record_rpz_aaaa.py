# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzAaaaResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_aaaa import READONLY_FIELDS, RecordRpzAaaa


class RecordRpzAaaaResource(WapiResource[RecordRpzAaaa]):
    """Manage NIOS RPZ AAAA record objects."""

    _wapi_type = "record:rpz:aaaa"
    _model = RecordRpzAaaa
    _default_return_fields = ["name", "ipv6addr", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
