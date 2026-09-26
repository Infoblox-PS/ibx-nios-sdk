# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcTopologyResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_topology import READONLY_FIELDS, DtcTopology


class DtcTopologyResource(WapiResource[DtcTopology]):
    """Manage NIOS DTC topology objects."""

    _wapi_type = "dtc:topology"
    _model = DtcTopology
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
