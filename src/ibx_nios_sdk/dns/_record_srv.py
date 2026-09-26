# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordSrv resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_srv import READONLY_FIELDS, RecordSrv


class RecordSrvResource(WapiResource[RecordSrv]):
    """Manage NIOS DNS SRV records (service location records)."""

    _wapi_type = "record:srv"
    _model = RecordSrv
    _default_return_fields = ["name", "port", "priority", "target", "weight", "view", "zone"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
