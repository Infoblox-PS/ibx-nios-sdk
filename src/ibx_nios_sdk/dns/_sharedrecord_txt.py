# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordTxt resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecord_txt import READONLY_FIELDS, SharedrecordTxt


class SharedrecordTxtResource(WapiResource[SharedrecordTxt]):
    """Manage NIOS shared DNS TXT records (text records shared across zones)."""

    _wapi_type = "sharedrecord:txt"
    _model = SharedrecordTxt
    _default_return_fields = ["name", "text", "shared_record_group", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
