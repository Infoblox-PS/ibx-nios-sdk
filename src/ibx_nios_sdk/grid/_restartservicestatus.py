# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RestartservicestatusResource - NIOS restart service status."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.restartservicestatus import READONLY_FIELDS, Restartservicestatus


class RestartservicestatusResource(WapiResource[Restartservicestatus]):
    """Access NIOS restart service status objects (read-only)."""

    _wapi_type = "restartservicestatus"
    _model = Restartservicestatus
    _default_return_fields = ["member", "dhcp_status", "dns_status", "reporting_status"]
    _readonly_fields = set(READONLY_FIELDS)
