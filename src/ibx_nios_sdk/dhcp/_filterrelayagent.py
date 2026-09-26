# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FilterrelayagentResource - DHCP relay agent filter."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dhcp.models.filterrelayagent import READONLY_FIELDS, Filterrelayagent


class FilterrelayagentResource(WapiResource[Filterrelayagent]):
    """Manage NIOS DHCP relay agent filter objects."""

    _wapi_type = "filterrelayagent"
    _model = Filterrelayagent
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
