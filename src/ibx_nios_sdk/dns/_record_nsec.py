# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNsec resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_nsec import READONLY_FIELDS, RecordNsec


class RecordNsecResource(WapiResource[RecordNsec]):
    """Manage NIOS DNS NSEC records (Next Secure records for DNSSEC)."""

    _wapi_type = "record:nsec"
    _model = RecordNsec
    _default_return_fields = ["name", "next_owner_name", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
