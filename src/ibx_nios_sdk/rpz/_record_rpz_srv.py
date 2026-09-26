# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzSrvResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_srv import READONLY_FIELDS, RecordRpzSrv


class RecordRpzSrvResource(WapiResource[RecordRpzSrv]):
    """Manage NIOS RPZ SRV record objects."""

    _wapi_type = "record:rpz:srv"
    _model = RecordRpzSrv
    _default_return_fields = ["name", "target", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
