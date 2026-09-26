# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordNaptr resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_naptr import READONLY_FIELDS, RecordNaptr


class RecordNaptrResource(WapiResource[RecordNaptr]):
    """Manage NIOS DNS NAPTR records (Naming Authority Pointer records)."""

    _wapi_type = "record:naptr"
    _model = RecordNaptr
    _default_return_fields = [
        "name",
        "order",
        "preference",
        "services",
        "regexp",
        "replacement",
        "view",
        "zone",
    ]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
