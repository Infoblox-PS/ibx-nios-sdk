# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RecordHostIpv4addrResource - standalone host IPv4 address resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.record_host_ipv4addr import READONLY_FIELDS, RecordHostIpv4addr


class RecordHostIpv4addrResource(WapiResource[RecordHostIpv4addr]):
    """Manage IPv4 address sub-records within NIOS host records."""

    _wapi_type = "record:host_ipv4addr"
    _model = RecordHostIpv4addr
    _default_return_fields = ["ipv4addr", "host"]
    _readonly_fields = set(READONLY_FIELDS)
