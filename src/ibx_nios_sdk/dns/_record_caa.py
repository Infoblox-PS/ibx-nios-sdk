# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordCaa resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_caa import READONLY_FIELDS, RecordCaa


class RecordCaaResource(WapiResource[RecordCaa]):
    """Manage NIOS DNS CAA records (Certification Authority Authorization)."""

    _wapi_type = "record:caa"
    _model = RecordCaa
    _default_return_fields = ["name", "ca_flag", "ca_tag", "ca_value", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
