# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNs resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_ns import READONLY_FIELDS, RecordNs


class RecordNsResource(WapiResource[RecordNs]):
    """Manage NIOS DNS NS records (authoritative name server records)."""

    _wapi_type = "record:ns"
    _model = RecordNs
    _default_return_fields = ["name", "nameserver", "view", "zone", "addresses"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"name", "view"}
