# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""BulkhostnametemplateResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.ipam.models.bulkhostnametemplate import (
    READONLY_FIELDS,
    Bulkhostnametemplate,
)


class BulkhostnametemplateResource(WapiResource[Bulkhostnametemplate]):
    """Manage NIOS IPAM bulk host name templates."""

    _wapi_type = "bulkhostnametemplate"
    _model = Bulkhostnametemplate
    _default_return_fields = ["template_name", "template_format"]
    _readonly_fields = set(READONLY_FIELDS)
