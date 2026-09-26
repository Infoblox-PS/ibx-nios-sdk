# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyLabelResource - GET only."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_topology_label import READONLY_FIELDS, DtcTopologyLabel


class DtcTopologyLabelResource(WapiResource[DtcTopologyLabel]):
    """Manage NIOS DTC topology label objects."""

    _wapi_type = "dtc:topology:label"
    _model = DtcTopologyLabel
    _default_return_fields = ["field", "label"]
    _readonly_fields = set(READONLY_FIELDS)
