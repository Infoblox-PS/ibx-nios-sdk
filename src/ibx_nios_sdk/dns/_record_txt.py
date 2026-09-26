# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordTxt resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_txt import READONLY_FIELDS, RecordTxt


class RecordTxtResource(WapiResource[RecordTxt]):
    """Manage NIOS DNS TXT records (free-form text records)."""

    _wapi_type = "record:txt"
    _model = RecordTxt
    _default_return_fields = ["name", "text", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
