# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostIpv6addrResource - standalone host IPv6 address resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_host_ipv6addr import READONLY_FIELDS, RecordHostIpv6addr


class RecordHostIpv6addrResource(WapiResource[RecordHostIpv6addr]):
    """Manage IPv6 address sub-records within NIOS host records."""

    _wapi_type = "record:host_ipv6addr"
    _model = RecordHostIpv6addr
    _default_return_fields = ["ipv6addr", "host"]
    _readonly_fields = set(READONLY_FIELDS)
