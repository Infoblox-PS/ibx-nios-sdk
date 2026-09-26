# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyRuleResource - GET+PUT (no POST/DELETE)."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_topology_rule import READONLY_FIELDS, DtcTopologyRule


class DtcTopologyRuleResource(WapiResource[DtcTopologyRule]):
    """Manage NIOS DTC topology rule objects."""

    _wapi_type = "dtc:topology:rule"
    _model = DtcTopologyRule
    _default_return_fields = ["dest_type", "return_type", "topology"]
    _readonly_fields = set(READONLY_FIELDS)
