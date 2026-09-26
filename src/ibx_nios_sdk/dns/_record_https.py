# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHttps resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_https import READONLY_FIELDS, RecordHttps


class RecordHttpsResource(WapiResource[RecordHttps]):
    """Manage NIOS DNS HTTPS records (service binding for HTTPS)."""

    _wapi_type = "record:https"
    _model = RecordHttps
    _default_return_fields = ["name", "priority", "target_name", "view", "zone", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"view"}
