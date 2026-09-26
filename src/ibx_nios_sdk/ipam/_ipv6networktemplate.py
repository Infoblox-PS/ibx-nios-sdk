# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6networktemplateResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.ipv6networktemplate import READONLY_FIELDS, Ipv6networktemplate


class Ipv6networktemplateResource(WapiResource[Ipv6networktemplate]):
    """Manage NIOS IPAM IPv6 network templates."""

    _wapi_type = "ipv6networktemplate"
    _model = Ipv6networktemplate
    _default_return_fields = ["name", "cidr", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
