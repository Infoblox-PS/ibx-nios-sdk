# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzCnameIpaddressResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_cname_ipaddress import (
    READONLY_FIELDS,
    RecordRpzCnameIpaddress,
)


class RecordRpzCnameIpaddressResource(WapiResource[RecordRpzCnameIpaddress]):
    """Manage NIOS RPZ CNAME IP-address substitution record objects."""

    _wapi_type = "record:rpz:cname:ipaddress"
    _model = RecordRpzCnameIpaddress
    _default_return_fields = ["name", "canonical", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
