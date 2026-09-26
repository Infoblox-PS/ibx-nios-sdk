# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzTxtResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_txt import READONLY_FIELDS, RecordRpzTxt


class RecordRpzTxtResource(WapiResource[RecordRpzTxt]):
    """Manage NIOS RPZ TXT record objects."""

    _wapi_type = "record:rpz:txt"
    _model = RecordRpzTxt
    _default_return_fields = ["name", "text", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
