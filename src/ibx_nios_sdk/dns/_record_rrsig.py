# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRrsig resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_rrsig import READONLY_FIELDS, RecordRrsig


class RecordRrsigResource(WapiResource[RecordRrsig]):
    """Manage NIOS DNS RRSIG records (DNSSEC resource record signatures)."""

    _wapi_type = "record:rrsig"
    _model = RecordRrsig
    _default_return_fields = ["name", "algorithm", "signer_name", "type_covered", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
