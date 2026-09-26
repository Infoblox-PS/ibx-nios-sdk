# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzNaptrResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_naptr import READONLY_FIELDS, RecordRpzNaptr


class RecordRpzNaptrResource(WapiResource[RecordRpzNaptr]):
    """Manage NIOS RPZ NAPTR record objects."""

    _wapi_type = "record:rpz:naptr"
    _model = RecordRpzNaptr
    _default_return_fields = ["name", "replacement", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
