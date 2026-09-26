# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneRp resource - Response Policy Zone CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_rp import READONLY_FIELDS, ZoneRp


class ZoneRpResource(WapiResource[ZoneRp]):
    """Manage NIOS DNS response policy zone (RPZ) configurations."""

    _wapi_type = "zone_rp"
    _model = ZoneRp
    _default_return_fields = [
        "fqdn",
        "view",
        "comment",
        "disable",
        "rpz_policy",
        "rpz_severity",
        "rpz_type",
    ]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"fqdn", "rpz_type"}
