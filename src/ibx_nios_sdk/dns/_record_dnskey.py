# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDnskey resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_dnskey import READONLY_FIELDS, RecordDnskey


class RecordDnskeyResource(WapiResource[RecordDnskey]):
    """Manage NIOS DNS DNSKEY records (DNSSEC public keys)."""

    _wapi_type = "record:dnskey"
    _model = RecordDnskey
    _default_return_fields = ["name", "algorithm", "key_tag", "view", "zone", "flags"]
    _readonly_fields = set(READONLY_FIELDS)
