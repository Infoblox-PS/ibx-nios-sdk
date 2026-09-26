# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzPtrResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_ptr import READONLY_FIELDS, RecordRpzPtr


class RecordRpzPtrResource(WapiResource[RecordRpzPtr]):
    """Manage NIOS RPZ PTR record objects."""

    _wapi_type = "record:rpz:ptr"
    _model = RecordRpzPtr
    _default_return_fields = ["name", "ptrdname", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
