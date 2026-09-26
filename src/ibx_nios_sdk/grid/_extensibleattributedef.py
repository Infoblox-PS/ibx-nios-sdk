# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ExtensibleattributedefResource - NIOS extensible attribute definition."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.grid.models.extensibleattributedef import READONLY_FIELDS, Extensibleattributedef


class ExtensibleattributedefResource(WapiResource[Extensibleattributedef]):
    """Manage NIOS extensible attribute definition objects."""

    _wapi_type = "extensibleattributedef"
    _model = Extensibleattributedef
    _default_return_fields = ["name", "type", "comment", "flags"]
    _readonly_fields = set(READONLY_FIELDS)
