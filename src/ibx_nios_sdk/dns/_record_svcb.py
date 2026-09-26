# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordSvcb resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_svcb import READONLY_FIELDS, RecordSvcb


class RecordSvcbResource(WapiResource[RecordSvcb]):
    """Manage NIOS DNS SVCB records (service binding records)."""

    _wapi_type = "record:svcb"
    _model = RecordSvcb
    _default_return_fields = ["name", "priority", "target_name", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
