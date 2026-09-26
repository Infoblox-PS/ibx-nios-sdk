# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DdnsPrincipalclusterGroup resource - DDNS principal cluster group CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.ddns_principalcluster_group import (
    READONLY_FIELDS,
    DdnsPrincipalclusterGroup,
)


class DdnsPrincipalclusterGroupResource(WapiResource[DdnsPrincipalclusterGroup]):
    """Manage NIOS DDNS principal cluster group configurations."""

    _wapi_type = "ddns:principalcluster:group"
    _model = DdnsPrincipalclusterGroup
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
