# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberDnsResource - NIOS member DNS properties."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.member_dns import READONLY_FIELDS, MemberDns


class MemberDnsResource(WapiResource[MemberDns]):
    """Manage NIOS member-level DNS property configurations."""

    _wapi_type = "member:dns"
    _model = MemberDns
    _default_return_fields = ["host_name", "ipv4addr", "ipv6addr", "dnssec_enabled"]
    _readonly_fields = set(READONLY_FIELDS)
