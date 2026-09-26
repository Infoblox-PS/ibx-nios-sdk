# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordAlias resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_alias import READONLY_FIELDS, RecordAlias


class RecordAliasResource(WapiResource[RecordAlias]):
    """Manage NIOS DNS ALIAS records (synthetic CNAME-like redirects)."""

    _wapi_type = "record:alias"
    _model = RecordAlias
    _default_return_fields = ["name", "target_name", "target_type", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
