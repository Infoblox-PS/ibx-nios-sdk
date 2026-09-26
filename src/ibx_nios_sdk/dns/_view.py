# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""View resource."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.view import READONLY_FIELDS, View


class ViewResource(WapiResource[View]):
    """Manage NIOS DNS views (resolution segmentation by query source)."""

    _wapi_type = "view"
    _model = View
    _default_return_fields = ["name", "is_default", "comment", "disable"]
    _readonly_fields = set(READONLY_FIELDS)
