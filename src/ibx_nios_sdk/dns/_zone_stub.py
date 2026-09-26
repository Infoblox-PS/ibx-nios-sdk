# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ZoneStub resource - stub DNS zone CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.zone_stub import READONLY_FIELDS, ZoneStub


class ZoneStubResource(WapiResource[ZoneStub]):
    """Manage NIOS stub DNS zone configurations."""

    _wapi_type = "zone_stub"
    _model = ZoneStub
    _default_return_fields = ["fqdn", "view", "comment", "disable", "stub_from"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"fqdn", "zone_format"}
