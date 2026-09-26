# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzMxResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_mx import READONLY_FIELDS, RecordRpzMx


class RecordRpzMxResource(WapiResource[RecordRpzMx]):
    """Manage NIOS RPZ MX record objects."""

    _wapi_type = "record:rpz:mx"
    _model = RecordRpzMx
    _default_return_fields = ["name", "mail_exchanger", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
