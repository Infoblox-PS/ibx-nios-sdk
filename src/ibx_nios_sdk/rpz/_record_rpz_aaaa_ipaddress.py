# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzAaaaIpaddressResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_aaaa_ipaddress import (
    READONLY_FIELDS,
    RecordRpzAaaaIpaddress,
)


class RecordRpzAaaaIpaddressResource(WapiResource[RecordRpzAaaaIpaddress]):
    """Manage NIOS RPZ AAAA IP-address substitution record objects."""

    _wapi_type = "record:rpz:aaaa:ipaddress"
    _model = RecordRpzAaaaIpaddress
    _default_return_fields = ["name", "ipv6addr", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
