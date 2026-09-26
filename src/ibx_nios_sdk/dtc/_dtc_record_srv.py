# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcRecordSrvResource - full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dtc.models.dtc_record_srv import READONLY_FIELDS, DtcRecordSrv


class DtcRecordSrvResource(WapiResource[DtcRecordSrv]):
    """Manage NIOS DTC SRV record objects."""

    _wapi_type = "dtc:record:srv"
    _model = DtcRecordSrv
    _default_return_fields = ["name", "target", "dtc_server", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"dtc_server"}
