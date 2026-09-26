# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordTlsa resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_tlsa import READONLY_FIELDS, RecordTlsa


class RecordTlsaResource(WapiResource[RecordTlsa]):
    """Manage NIOS DNS TLSA records (TLS authentication via DANE)."""

    _wapi_type = "record:tlsa"
    _model = RecordTlsa
    _default_return_fields = [
        "name",
        "certificate_usage",
        "selector",
        "matched_type",
        "view",
        "zone",
    ]
    _readonly_fields = set(READONLY_FIELDS)
