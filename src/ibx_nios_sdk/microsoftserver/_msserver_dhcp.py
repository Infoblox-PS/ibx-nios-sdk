# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverDhcpResource - NIOS MS server DHCP, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.microsoftserver.models.msserver_dhcp import READONLY_FIELDS, MsserverDhcp


class MsserverDhcpResource(WapiResource[MsserverDhcp]):
    """Manage NIOS Microsoft server DHCP configuration objects."""

    _wapi_type = "msserver:dhcp"
    _model = MsserverDhcp
    _default_return_fields = ["address", "server_name", "status"]
    _readonly_fields = set(READONLY_FIELDS)
