# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DdnsPrincipalcluster resource - DDNS principal cluster CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.ddns_principalcluster import (
    READONLY_FIELDS,
    DdnsPrincipalcluster,
)


class DdnsPrincipalclusterResource(WapiResource[DdnsPrincipalcluster]):
    """Manage NIOS DDNS principal cluster configurations."""

    _wapi_type = "ddns:principalcluster"
    _model = DdnsPrincipalcluster
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
