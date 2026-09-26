# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcAllrecordsResource - aggregate read-only record view."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_allrecords import READONLY_FIELDS, DtcAllrecords


class DtcAllrecordsResource(WapiResource[DtcAllrecords]):
    """Access NIOS DTC all-records aggregate (read-only)."""

    _wapi_type = "dtc:allrecords"
    _model = DtcAllrecords
    _default_return_fields = ["dtc_server", "type", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
