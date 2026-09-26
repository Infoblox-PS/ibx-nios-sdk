# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordCname resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_cname import READONLY_FIELDS, RecordCname


class RecordCnameResource(WapiResource[RecordCname]):
    """Manage NIOS DNS CNAME records (canonical name aliases)."""

    _wapi_type = "record:cname"
    _model = RecordCname
    _default_return_fields = ["name", "canonical", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
