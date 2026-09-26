# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordRpzCnameClientipaddressdnResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.rpz.models.record_rpz_cname_clientipaddressdn import (
    READONLY_FIELDS,
    RecordRpzCnameClientipaddressdn,
)


class RecordRpzCnameClientipaddressdnResource(WapiResource[RecordRpzCnameClientipaddressdn]):
    """Manage NIOS RPZ CNAME client-IP-address domain-name substitution record objects."""

    _wapi_type = "record:rpz:cname:clientipaddressdn"
    _model = RecordRpzCnameClientipaddressdn
    _default_return_fields = ["name", "canonical", "view", "zone", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
