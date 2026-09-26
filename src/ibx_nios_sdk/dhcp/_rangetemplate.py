# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RangetemplateResource - DHCP IPv4 range template."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.rangetemplate import READONLY_FIELDS, Rangetemplate


class RangetemplateResource(WapiResource[Rangetemplate]):
    """Manage NIOS DHCP range template objects."""

    _wapi_type = "rangetemplate"
    _model = Rangetemplate
    _default_return_fields = ["name", "number_of_addresses", "offset", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
