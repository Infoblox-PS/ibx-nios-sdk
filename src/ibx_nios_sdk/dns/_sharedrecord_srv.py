# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""SharedrecordSrv resource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.sharedrecord_srv import READONLY_FIELDS, SharedrecordSrv


class SharedrecordSrvResource(WapiResource[SharedrecordSrv]):
    """Manage NIOS shared DNS SRV records (service locations shared across zones)."""

    _wapi_type = "sharedrecord:srv"
    _model = SharedrecordSrv
    _default_return_fields = [
        "name",
        "port",
        "priority",
        "target",
        "weight",
        "shared_record_group",
    ]
    _readonly_fields = set(READONLY_FIELDS)
