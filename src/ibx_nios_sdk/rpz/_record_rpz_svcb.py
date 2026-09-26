# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzSvcbResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_svcb import READONLY_FIELDS, RecordRpzSvcb


class RecordRpzSvcbResource(WapiResource[RecordRpzSvcb]):
    """Manage NIOS RPZ SVCB record objects."""

    _wapi_type = "record:rpz:svcb"
    _model = RecordRpzSvcb
    _default_return_fields = ["name", "target_name", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
