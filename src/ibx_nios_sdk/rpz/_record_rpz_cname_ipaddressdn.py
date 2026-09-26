# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzCnameIpaddressdnResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_cname_ipaddressdn import (
    READONLY_FIELDS,
    RecordRpzCnameIpaddressdn,
)


class RecordRpzCnameIpaddressdnResource(WapiResource[RecordRpzCnameIpaddressdn]):
    """Manage NIOS RPZ CNAME IP-address domain-name substitution record objects."""

    _wapi_type = "record:rpz:cname:ipaddressdn"
    _model = RecordRpzCnameIpaddressdn
    _default_return_fields = ["name", "canonical", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
