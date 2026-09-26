# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneDelegated resource - delegated DNS zone CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_delegated import READONLY_FIELDS, ZoneDelegated


class ZoneDelegatedResource(WapiResource[ZoneDelegated]):
    """Manage NIOS delegated DNS zone configurations."""

    _wapi_type = "zone_delegated"
    _model = ZoneDelegated
    _default_return_fields = ["fqdn", "view", "comment", "disable", "delegate_to"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"fqdn", "zone_format"}
