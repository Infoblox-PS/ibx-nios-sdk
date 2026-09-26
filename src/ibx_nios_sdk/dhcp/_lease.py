# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""LeaseResource - DHCP lease (read-only aggregate)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.lease import READONLY_FIELDS, Lease


class LeaseResource(WapiResource[Lease]):
    """Access NIOS DHCP lease objects (read-only)."""

    _wapi_type = "lease"
    _model = Lease
    _default_return_fields = ["address", "hardware", "client_hostname", "binding_state"]
    _readonly_fields = set(READONLY_FIELDS)
