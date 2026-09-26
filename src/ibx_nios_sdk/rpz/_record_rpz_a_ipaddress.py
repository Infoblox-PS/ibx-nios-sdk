# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzAIpaddressResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_a_ipaddress import READONLY_FIELDS, RecordRpzAIpaddress


class RecordRpzAIpaddressResource(WapiResource[RecordRpzAIpaddress]):
    """Manage NIOS RPZ A IP-address substitution record objects."""

    _wapi_type = "record:rpz:a:ipaddress"
    _model = RecordRpzAIpaddress
    _default_return_fields = ["name", "ipv4addr", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
