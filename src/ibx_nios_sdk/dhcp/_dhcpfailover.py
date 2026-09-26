# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DhcpfailoverResource - DHCP failover configuration."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.dhcpfailover import READONLY_FIELDS, Dhcpfailover


class DhcpfailoverResource(WapiResource[Dhcpfailover]):
    """Manage NIOS DHCP failover association objects."""

    _wapi_type = "dhcpfailover"
    _model = Dhcpfailover
    _default_return_fields = ["name", "primary", "secondary", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"ms_failover_partner", "ms_server"}
