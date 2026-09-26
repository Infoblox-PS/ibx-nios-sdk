# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzHttpsResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_https import READONLY_FIELDS, RecordRpzHttps


class RecordRpzHttpsResource(WapiResource[RecordRpzHttps]):
    """Manage NIOS RPZ HTTPS record objects."""

    _wapi_type = "record:rpz:https"
    _model = RecordRpzHttps
    _default_return_fields = ["name", "target_name", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
