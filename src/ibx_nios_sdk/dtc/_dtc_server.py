# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcServerResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_server import READONLY_FIELDS, DtcServer


class DtcServerResource(WapiResource[DtcServer]):
    """Manage NIOS DTC server objects."""

    _wapi_type = "dtc:server"
    _model = DtcServer
    _default_return_fields = ["name", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
