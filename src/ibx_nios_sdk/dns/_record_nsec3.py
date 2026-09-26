# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNsec3 resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_nsec3 import READONLY_FIELDS, RecordNsec3


class RecordNsec3Resource(WapiResource[RecordNsec3]):
    """Manage NIOS DNS NSEC3 records (Next Secure v3 records for DNSSEC)."""

    _wapi_type = "record:nsec3"
    _model = RecordNsec3
    _default_return_fields = ["name", "algorithm", "iterations", "salt", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
