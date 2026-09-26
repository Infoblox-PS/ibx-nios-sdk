# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDs resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_ds import READONLY_FIELDS, RecordDs


class RecordDsResource(WapiResource[RecordDs]):
    """Manage NIOS DNS DS records (DNSSEC Delegation Signer records)."""

    _wapi_type = "record:ds"
    _model = RecordDs
    _default_return_fields = ["name", "algorithm", "digest_type", "key_tag", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
