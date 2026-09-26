# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzCnameResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_cname import READONLY_FIELDS, RecordRpzCname


class RecordRpzCnameResource(WapiResource[RecordRpzCname]):
    """Manage NIOS RPZ CNAME record objects."""

    _wapi_type = "record:rpz:cname"
    _model = RecordRpzCname
    _default_return_fields = ["name", "canonical", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
