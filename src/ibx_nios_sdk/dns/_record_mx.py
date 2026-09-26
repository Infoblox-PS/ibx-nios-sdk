# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordMx resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_mx import READONLY_FIELDS, RecordMx


class RecordMxResource(WapiResource[RecordMx]):
    """Manage NIOS DNS MX records (mail exchanger records)."""

    _wapi_type = "record:mx"
    _model = RecordMx
    _default_return_fields = ["name", "mail_exchanger", "preference", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
