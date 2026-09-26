# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FixedaddresstemplateResource - DHCP IPv4 fixed address template."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.fixedaddresstemplate import READONLY_FIELDS, Fixedaddresstemplate


class FixedaddresstemplateResource(WapiResource[Fixedaddresstemplate]):
    """Manage NIOS DHCP fixed address template objects."""

    _wapi_type = "fixedaddresstemplate"
    _model = Fixedaddresstemplate
    _default_return_fields = ["name", "number_of_addresses", "offset", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
