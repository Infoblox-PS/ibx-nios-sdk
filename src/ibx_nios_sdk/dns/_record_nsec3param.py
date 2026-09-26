# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNsec3param resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_nsec3param import READONLY_FIELDS, RecordNsec3param


class RecordNsec3paramResource(WapiResource[RecordNsec3param]):
    """Manage NIOS DNS NSEC3PARAM records (DNSSEC NSEC3 parameter records)."""

    _wapi_type = "record:nsec3param"
    _model = RecordNsec3param
    _default_return_fields = ["name", "algorithm", "iterations", "salt", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
