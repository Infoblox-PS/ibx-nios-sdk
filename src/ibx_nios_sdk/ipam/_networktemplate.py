# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NetworktemplateResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.networktemplate import READONLY_FIELDS, Networktemplate


class NetworktemplateResource(WapiResource[Networktemplate]):
    """Manage NIOS IPAM IPv4 network templates."""

    _wapi_type = "networktemplate"
    _model = Networktemplate
    _default_return_fields = ["name", "netmask", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
