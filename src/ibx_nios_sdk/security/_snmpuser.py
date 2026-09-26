# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SnmpuserResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.snmpuser import READONLY_FIELDS, Snmpuser


class SnmpuserResource(WapiResource[Snmpuser]):
    """Manage NIOS SNMP user objects."""

    _wapi_type = "snmpuser"
    _model = Snmpuser
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
