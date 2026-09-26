# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Sharedrecordgroup resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecordgroup import READONLY_FIELDS, Sharedrecordgroup


class SharedrecordgroupResource(WapiResource[Sharedrecordgroup]):
    """Manage NIOS shared DNS record groups (containers for shared records)."""

    _wapi_type = "sharedrecordgroup"
    _model = Sharedrecordgroup
    _default_return_fields = ["name", "record_name_policy", "use_record_name_policy", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
