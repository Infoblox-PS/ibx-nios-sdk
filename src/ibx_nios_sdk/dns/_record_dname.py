# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordDname resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_dname import READONLY_FIELDS, RecordDname


class RecordDnameResource(WapiResource[RecordDname]):
    """Manage NIOS DNS DNAME records (DNS name subtree delegations)."""

    _wapi_type = "record:dname"
    _model = RecordDname
    _default_return_fields = ["name", "target", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
