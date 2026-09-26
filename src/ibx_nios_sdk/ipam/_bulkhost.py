# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""BulkhostResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.bulkhost import READONLY_FIELDS, Bulkhost


class BulkhostResource(WapiResource[Bulkhost]):
    """Manage NIOS IPAM bulk host objects."""

    _wapi_type = "bulkhost"
    _model = Bulkhost
    _default_return_fields = ["prefix", "start_addr", "end_addr", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
