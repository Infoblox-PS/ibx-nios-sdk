# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MsserverDnsResource - NIOS MS server DNS, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.microsoftserver.models.msserver_dns import READONLY_FIELDS, MsserverDns


class MsserverDnsResource(WapiResource[MsserverDns]):
    """Manage NIOS Microsoft server DNS configuration objects."""

    _wapi_type = "msserver:dns"
    _model = MsserverDns
    _default_return_fields = ["address", "uuid"]
    _readonly_fields = set(READONLY_FIELDS)
