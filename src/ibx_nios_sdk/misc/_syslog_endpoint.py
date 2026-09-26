# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SyslogEndpointResource - NIOS syslog endpoint, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.syslog_endpoint import READONLY_FIELDS, SyslogEndpoint


class SyslogEndpointResource(WapiResource[SyslogEndpoint]):
    """Manage NIOS syslog endpoint objects."""

    _wapi_type = "syslog:endpoint"
    _model = SyslogEndpoint
    _default_return_fields = ["name", "log_level", "timeout"]
    _readonly_fields = set(READONLY_FIELDS)
