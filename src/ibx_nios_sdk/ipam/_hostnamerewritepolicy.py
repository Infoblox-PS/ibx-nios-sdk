# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""HostnamerewritepolicyResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.hostnamerewritepolicy import (
    READONLY_FIELDS,
    Hostnamerewritepolicy,
)


class HostnamerewritepolicyResource(WapiResource[Hostnamerewritepolicy]):
    """Manage NIOS IPAM hostname rewrite policy configurations."""

    _wapi_type = "hostnamerewritepolicy"
    _model = Hostnamerewritepolicy
    _default_return_fields = ["name"]
    _readonly_fields = set(READONLY_FIELDS)
