# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Recordnamepolicy resource - DNS record name policy CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.recordnamepolicy import READONLY_FIELDS, Recordnamepolicy


class RecordnamepolicyResource(WapiResource[Recordnamepolicy]):
    """Manage NIOS DNS record-name policy configurations."""

    _wapi_type = "recordnamepolicy"
    _model = Recordnamepolicy
    _default_return_fields = ["name", "is_default", "regex"]
    _readonly_fields = set(READONLY_FIELDS)
