# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_host import READONLY_FIELDS, RecordHost


class RecordHostResource(WapiResource[RecordHost]):
    """Manage NIOS DNS host records (combined A/AAAA/PTR under one name)."""

    _wapi_type = "record:host"
    _model = RecordHost
    _default_return_fields = ["name", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"network_view"}
